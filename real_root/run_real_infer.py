"""对 5 个真实件跑 CAD-Recode 与 cadrille(pc): monkeypatch 两个复现脚本的路径常量,
输入 real_root/output/<name>/point_cloud.npy, 输出 real_root/predictions/{cadrecode,cadrille}/。
用法: python run_real_infer.py cadrecode|cadrille
"""
import os, sys

REAL = "E:/3005/data/real_root"
which = sys.argv[1]

if which == "cadrecode":
    sys.path.insert(0, "E:/3005/data/cadrecode_repro")
    sys.argv = ["run_cadrecode.py"]          # 清参, 免得 argparse 吃到 which
    import run_cadrecode as rc
    rc.OUTDIR = os.path.join(REAL, "output")
    rc.SUBSET = os.path.join(REAL, "names.txt")
    rc.PRED = os.path.join(REAL, "predictions", "cadrecode")
    rc.main()
elif which == "cadrille":
    # transformers>=4.52 把 embed_tokens 挪进 language_model; 老版本实例自带, 带回退
    from transformers.models.qwen2_vl.modeling_qwen2_vl import Qwen2VLModel
    if not hasattr(Qwen2VLModel, "embed_tokens"):
        Qwen2VLModel.embed_tokens = property(
            lambda self: self._modules.get("embed_tokens")
            or self.language_model.embed_tokens)
    sys.path.insert(0, "E:/3005/data/cadrille_repro")
    sys.argv = ["run_cadrille.py", "--names-file", os.path.join(REAL, "names.txt"),
                "--mode", "pc", "--chunk", "5"]
    import run_cadrille as rc
    rc.ROOT = REAL                            # pred_dir = REAL/predictions/cadrille
    rc.OUTDIR = os.path.join(REAL, "output")
    rc.main()
else:
    raise SystemExit("cadrecode|cadrille")
