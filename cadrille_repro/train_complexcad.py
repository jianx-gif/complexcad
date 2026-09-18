# -*- coding: utf-8 -*-
"""实验H: cadrille 在 ComplexCAD 上的 LoRA 微调 pilot (批注p51/p55 训练消融).
从发布 checkpoint (maksimko123/cadrille) 出发, LoRA 只训 LLM 投影层;
2000 件 pilot 训练集(_review/cc_ft), pc 模式, 12GB 显存配置
(batch1 x accum8, 梯度检查点, bf16), 断点续训 + GPU 温控.
"""
import os
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF', 'expandable_segments:True')
import time
import subprocess
from functools import partial

import torch
from transformers import AutoProcessor, Trainer, TrainingArguments, TrainerCallback
from peft import LoraConfig, get_peft_model

from cadrille import Cadrille, collate
from dataset import CadRecodeDataset

DATA = r'E:/3005/data/_review/cc_ft'
OUT = r'E:/3005/data/_review/cc_ft_lora'
MODEL_ID = 'maksimko123/cadrille'
MAXTEMP = 82


def gpu_temp():
    try:
        return int(subprocess.run(
            ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader'],
            capture_output=True, text=True, timeout=10).stdout.strip().split('\n')[0])
    except Exception:
        return -1


class TempGuard(TrainerCallback):
    def on_step_end(self, args, state, control, **kwargs):
        if state.global_step % 25 == 0:
            t = gpu_temp()
            if t >= MAXTEMP:
                print(f'[temp] GPU {t}C >= {MAXTEMP}C, cool 60s', flush=True)
                torch.cuda.empty_cache()
                time.sleep(60)


class LogFile(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kwargs):
        with open(os.path.join(OUT, 'log.txt'), 'a', encoding='utf-8') as f:
            f.write(f'{state.global_step} {logs}\n')


def main():
    os.makedirs(OUT, exist_ok=True)
    processor = AutoProcessor.from_pretrained(
        'Qwen/Qwen2-VL-2B-Instruct',
        min_pixels=256 * 28 * 28, max_pixels=1280 * 28 * 28, padding_side='left')
    model = Cadrille.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, attn_implementation='sdpa')
    model.config.use_cache = False
    model.enable_input_require_grads()   # 梯度检查点+LoRA: 输入须带grad

    lora = LoraConfig(
        r=16, lora_alpha=32, lora_dropout=0.05, bias='none',
        target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj',
                        'gate_proj', 'up_proj', 'down_proj'])
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()

    ds_kw = dict(n_points=256, normalize_std_pc=100, noise_scale_pc=0.01,
                 img_size=128, normalize_std_img=200, noise_scale_img=-1,
                 num_imgs=4, mode='pc')
    train_ds = CadRecodeDataset(root_dir=DATA, split='train', **ds_kw)
    val_kw = dict(ds_kw, noise_scale_pc=None)
    val_ds = CadRecodeDataset(root_dir=DATA, split='val', **val_kw)
    print('train', len(train_ds), 'val', len(val_ds), flush=True)

    resume = any(d.startswith('checkpoint-') for d in os.listdir(OUT))
    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir=OUT,
            per_device_train_batch_size=1,
            gradient_accumulation_steps=8,
            gradient_checkpointing=True,
            gradient_checkpointing_kwargs={'use_reentrant': False},
            dataloader_num_workers=2,
            num_train_epochs=2,
            lr_scheduler_type='cosine',
            learning_rate=1e-4,
            warmup_steps=50,
            weight_decay=0.01,
            bf16=True,
            remove_unused_columns=False,
            logging_steps=20,
            save_total_limit=2,
            save_strategy='steps',
            save_steps=100,
            eval_strategy='no',
            report_to=[]),
        train_dataset=train_ds,
        eval_dataset=val_ds,
        data_collator=partial(collate, processor=processor, n_points=256),
        callbacks=[TempGuard(), LogFile()])
    trainer.train(resume_from_checkpoint=resume)
    model.save_pretrained(os.path.join(OUT, 'final_adapter'))
    print('TRAINING DONE ->', os.path.join(OUT, 'final_adapter'), flush=True)


if __name__ == '__main__':
    main()
