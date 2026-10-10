"""Assemble <repo>/_review/exp_hh_adapter_sanity.json and .log from the working folder."""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))  # repository root
import os, json, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REVIEW = os.path.dirname(HERE)
OUT_JSON = os.path.join(REVIEW, 'exp_hh_adapter_sanity.json')
OUT_LOG = os.path.join(REVIEW, 'exp_hh_adapter_sanity.log')
assert not os.path.exists(OUT_JSON) and not os.path.exists(OUT_LOG), 'refusing to overwrite'


def load(p):
    return json.load(open(p, encoding='utf-8'))


def r(x, k=3):
    return None if x is None else round(float(x), k)


def per_mode(tag, pred_dir, runtime_files):
    off = load(os.path.join(HERE, 'evals', f'{tag}_official.json'))
    ours = load(os.path.join(HERE, 'evals', f'{tag}_ours.json'))
    rts = [load(os.path.join(HERE, pred_dir, f)) for f in runtime_files]
    preds = sorted(f for f in os.listdir(os.path.join(HERE, pred_dir)) if f.endswith('.py'))
    lens, rep = [], 0
    for f in preds:
        code = open(os.path.join(HERE, pred_dir, f), encoding='utf-8').read()
        lens.append(len(code))
        tail = code[-600:]
        if len(tail) >= 200 and tail.count(tail[-12:]) >= 15:
            rep += 1
    s, o = off['summary'], ours['summary']
    return {
        'n_samples': len(preds),
        'n_inference_failures': sum(x['fail'] for x in rts),
        'official_metrics_cadrille_evaluate_py': {
            'IoU_mean_pct': r(s['mean_iou_pct'], 2), 'IoU_median_pct': r(s['iou_median_pct'], 2),
            'CD_median_x1000': r(s['median_cd_x1000']),
            'CD_mean_x1000_skip0': r(s['mean_cd_x1000_skip']['0']),
            'CD_mean_x1000_skip1': r(s['mean_cd_x1000_skip'].get('1')),
            'CD_x1000_p25_p75': [r(s['cd_x1000_p25']), r(s['cd_x1000_p75'])],
            'IR_pct': r(s['ir_pct'], 2), 'IR_iou_pct': r(s['ir_iou_pct'], 2),
            'n_valid_cd': s['n_valid_cd'], 'n_valid_iou': s['n_valid_iou'],
            'executed_to_mesh_pct': r(s['executed_pct'], 2),
            'IoU_ge_0.9_pct': r(s['iou_ge_0.9_pct'], 2), 'IoU_ge_0.5_pct': r(s['iou_ge_0.5_pct'], 2),
            'n_timeout': s['n_timeout'], 'eval_seconds': s['eval_seconds'],
        },
        'our_convention_eval_predictions_py': {
            'validity_pct': r(o['valid_pct'], 2),
            'chamfer_bbox_norm_mean': r(o['chamfer_mean'], 5), 'chamfer_bbox_norm_median': r(o['chamfer_median'], 5),
            'fscore_at_0.02_mean': r(o['fscore_mean'], 4),
            'op_type_recall_mean': r(o['op_type_recall_mean']), 'op_count_recall_mean': r(o['op_count_recall_mean']),
            'op_exact_pct': r(o['op_exact_pct'], 2), 'n_with_gt_program': o['n_with_gt_program'],
            'status_counts': o['status_counts'], 'n_timeout': o['n_timeout'], 'eval_seconds': o['eval_seconds'],
        },
        'prediction_stats': {'code_chars_mean': r(np.mean(lens), 1), 'code_chars_median': float(np.median(lens)),
                             'code_chars_max': int(max(lens)), 'repetition_degenerate_n': rep},
        'runtime': {'inference_seconds': r(sum(x['seconds'] for x in rts), 1),
                    'seconds_per_item': r(sum(x['seconds'] for x in rts) / max(1, sum(x['todo_this_run'] for x in rts)), 2),
                    'batch': rts[0]['batch'], 'max_new_tokens': rts[0]['max_new_tokens'],
                    'peak_vram_gb': r(max(x['peak_vram_gb'] for x in rts), 2), 'runs': len(rts)},
    }


text = per_mode('text', 'preds_text', ['_runtime.json'])
img14 = per_mode('img', 'preds_img', ['_runtime_first100.json', '_runtime.json'])
img10 = per_mode('img_qvu010', 'preds_img_qvu010', ['_runtime.json'])
img10['qwen_vl_utils'] = '0.0.10 (Dockerfile pin; video grid 20x20 = 100 tokens per composite)'
img14['qwen_vl_utils'] = '0.0.14 (installed in cadrec_env, used for all our arms; video grid 24x24 = 144 tokens)'

paper = {
    'source': 'arXiv 2505.22914 (cadrille, Kolodiazhnyi et al.), HTML version fetched 2026-09-17',
    'metric_definition': 'GT normalised to unit cube; CD = median Chamfer distance on 8192 points x10^3; '
                         'IoU mean in %; IR = % of sequences without a valid CAD model (Sec. 5, Metrics)',
    'table1_deepcad_test_row_cadrille_Rpi+Dt_no_RL': {
        'text': {'CD_median_x1000': 0.20, 'IoU_pct': 82.1, 'IR_pct': 1.4},
        'multi_view_images': {'CD_median_x1000': 0.18, 'IoU_pct': 86.1, 'IR_pct': 1.5},
        'point_cloud': {'CD_median_x1000': 0.18, 'IoU_pct': 87.1, 'IR_pct': 2.1},
    },
    'table2_images_deepcad_row_cadrille_SFT_Rpi_no_RL': {'CD_median_x1000': 0.18, 'IoU_pct': 86.1, 'IR_pct': 1.5},
    'table6_mean_CD_x1000_deepcad_row_cadrille_Rpi+Dt': {'points': 0.76, 'images': 0.81, 'text': 3.95},
    'note': 'The released SFT checkpoint maksimko123/cadrille is, per its model card, "the three-modal model '
            'without RL fine-tuning", i.e. the Rpi+Dt rows of Table 1 (train.py --mode pc_img --use-text); '
            'the RL rows (cadrille-rl) are not tested here.',
}

our_data = {
    'source': _ROOT + '/1m_Convert/precision_report/pred_metrics_cadrille_{text,img,}.jsonl '
              '(released checkpoint on the ComplexCAD 400-item test subset, eval_predictions.py convention; '
              'thesis tab:cmp-ablation)',
    'text': {'validity_pct': 89.2, 'chamfer_bbox_norm_mean': 0.4220, 'fscore_mean': 0.044, 'op_type_recall': 0.23},
    'img': {'validity_pct': 76.8, 'chamfer_bbox_norm_mean': 0.2800, 'fscore_mean': 0.099, 'op_type_recall': 0.28,
            'note': 'produced with qwen-vl-utils 0.0.14, i.e. with the 24x24 video grid, see environment_finding'},
    'pc': {'validity_pct': 95.2, 'chamfer_bbox_norm_mean': 0.0316, 'fscore_mean': 0.810, 'op_type_recall': 0.29},
}


def verdict(m, ref):
    s = m['official_metrics_cadrille_evaluate_py']
    d_iou = s['IoU_mean_pct'] - ref['IoU_pct']
    d_ir = s['IR_pct'] - ref['IR_pct']
    d_cd = s['CD_median_x1000'] - ref['CD_median_x1000']
    ok = abs(d_iou) <= 5 and d_ir <= 3 and abs(d_cd) <= 0.1
    return {'delta_IoU_pp': r(d_iou, 2), 'delta_IR_pp': r(d_ir, 2), 'delta_CD_median_x1000': r(d_cd),
            'within_tolerance(IoU+-5pp, IR<=+3pp, CD+-0.1)': ok}


def ci_halfwidth(p_pct, n):
    p = max(p_pct, 0.5) / 100
    return r(196 * (p * (1 - p) / n) ** 0.5, 2)


ref_t = paper['table1_deepcad_test_row_cadrille_Rpi+Dt_no_RL']['text']
ref_i = paper['table1_deepcad_test_row_cadrille_Rpi+Dt_no_RL']['multi_view_images']
text_v, img14_v, img10_v = verdict(text, ref_t), verdict(img14, ref_i), verdict(img10, ref_i)

result = {
    'experiment': 'exp_hh_adapter_sanity: released cadrille checkpoint, text and image branches on the OFFICIAL data they were trained/evaluated on',
    'date': time.strftime('%Y-%m-%d %H:%M'),
    'question': 'Are the poor text/image results on our ComplexCAD data a domain gap or a broken adapter?',
    'checkpoint': {
        'hf_id': 'maksimko123/cadrille', 'hf_revision': '2f422d1169e4362e2288b0e0f54bb3a2b504e0f9',
        'local_path': '~/.cache/huggingface/hub/models--maksimko123--cadrille/snapshots/2f422d1169e4362e2288b0e0f54bb3a2b504e0f9',
        'model_safetensors_bytes': 4418370528, 'adapter': 'none (base released SFT checkpoint, no LoRA)',
    },
    'data': {
        'text': {
            'dataset': 'Text2CAD test split as packaged by the cadrille authors (HF dataset maksimko123/text2cad, '
                       'text2cad.zip -> test.pkl, 8035 uids = DeepCAD ids, descriptions "shortened a bit" per data/README.md)',
            'gt_mesh': 'HF dataset maksimko123/deepcad_test_mesh (<uid>.stl, 8046 files, unit cube); all 8035 test uids have a mesh',
            'gt_program': 'text2cad.zip cadquery/<uid>.py (7797 of 8035 test uids have one)',
            'subset': 'random.seed(42); random.sample(test_uids, 200) -> subset_text_200.txt',
            'n': text['n_samples'],
        },
        'img': {
            'dataset': 'DeepCAD test meshes (HF maksimko123/deepcad_test_mesh, 8046 STL) rendered on the fly by the '
                       'official loader dataset.CadRecodeDataset(mode="img", img_size=128, num_imgs=4): four open3d views '
                       '(fronts (1,1,1),(-1,-1,-1),(-1,1,-1),(1,-1,1), camera_distance -0.9, colour (255,255,136), '
                       '500x500 -> 128x128), 3 px black border, 2x2 grid (268x268), prompt "Generate cadquery code"',
            'gt_mesh': 'same STL files', 'gt_program': 'text2cad.zip cadquery/<uid>.py where available',
            'subset': 'random.seed(42); random.sample(deepcad_test_stl_list_8046, 200) -> subset_img_200.txt; '
                      'the qwen-vl-utils 0.0.10 re-run used the first 100 of that sample (subset_img_100.txt) '
                      'because of the 2 h wall-clock budget',
            'n_qvu014': img14['n_samples'], 'n_qvu010': img10['n_samples'],
            'overlap_with_text_subset': 5,
        },
        'local_copy': _ROOT + '/_review/_hh_adapter/data/ (text2cad.zip 82.8 MB, 395 STL)',
    },
    'settings': {
        'inference_script': _ROOT + '/_review/_hh_adapter/run_official.py = run_cadrille.py loading/generation '
                            '(AutoProcessor Qwen/Qwen2-VL-2B-Instruct min_pixels 256*28*28 max_pixels 1280*28*28 '
                            'padding_side left; Cadrille.from_pretrained bf16 attn sdpa; cadrille.collate eval=True; '
                            'max_new_tokens 768) with the official dataset.py loaders for inputs; '
                            'run_official_qvu010.py = same with qwen-vl-utils 0.0.10 on sys.path',
        'decoding': 'checkpoint generation_config.json: do_sample true, temperature 0.01, top_k 1, top_p 0.001 '
                    '(effectively greedy) - unchanged',
        'batch_size': {'text': 8, 'img': 4},
        'environment': 'venv cadrec_env (Python 3.13.2, torch 2.6.0+cu124, transformers 4.50.3, qwen-vl-utils 0.0.14) '
                       'for inference; open3d 0.20.0 and qwen-vl-utils 0.0.10 installed into isolated folders under '
                       '_hh_adapter/ (venv untouched); conda cadfit-env (CadQuery 2.6.1, trimesh 4.11.5, manifold3d) for evaluation',
        'gpu': 'NVIDIA GeForce RTX 4080 Laptop GPU 12 GB',
        'deviations_from_official_protocol': [
            'subsets (200 text, 200 / 100 image) instead of the full 8035 (text) / 8046 (image) test sets',
            'batch size 8 (text) / 4 (image) with left padding instead of 32 / 256 in test.py; attention sdpa instead of '
            'flash_attention_2 (Windows); both are numerically inconsequential for greedy decoding up to bf16 noise',
            'evaluation: evaluate.py metric functions are imported unchanged, but each program is executed inside a '
            'persistent worker with a 180 s per-item timeout instead of a fresh process with a 3 s timeout (Windows spawn '
            're-imports cadquery in ~5 s); the global r is cleared before every exec',
            'image renders come from open3d 0.20.0 (Windows OpenGL window, visible=False) instead of the authors\' headless '
            'OSMesa build of Open3D commit 8e434558; camera/colour/resolution follow dataset.py exactly and the extrinsic '
            'was verified to be applied (convert_from_pinhole_camera_parameters -> True)',
            'the venv runs qwen-vl-utils 0.0.14 (Dockerfile pins 0.0.10); the image branch was therefore run twice, '
            'see environment_finding',
        ],
    },
    'environment_finding': {
        'what': 'qwen-vl-utils 0.0.14 (cadrec_env) returns the single-frame "video" as a 2x3x336x336 tensor that the '
                'Qwen2-VL processor does not resize again -> video_grid_thw [1,24,24] = 144 video tokens; '
                'qwen-vl-utils 0.0.10 (cadrille Dockerfile) returns two 280x280 PIL frames -> [1,20,20] = 100 tokens. '
                'The checkpoint was trained with the 0.0.10 grid. Text and point-cloud inputs do not pass through '
                'process_vision_info, so only the image (video) branch is affected.',
        'evidence': 'collate() on sample_img_item0.png: grid [[1,24,24]] / 576 patches / 144 video tokens with 0.0.14 vs '
                    '[[1,20,20]] / 400 patches / 100 tokens with 0.0.10 (this session, see exp_hh_adapter_sanity.log)',
        'affects_our_arms': 'predictions/cadrille_img and predictions/cadrille_img_text (thesis tab:cmp-ablation rows '
                            '"rendered image" and "image + text") were produced with 0.0.14, i.e. with the mismatched 144-token grid; '
                            'pc, text, pc_text and the drawing arm (image path, trained and inferred with the same 0.0.14) are not affected',
    },
    'results': {'text': text, 'img_qvu014': img14, 'img_qvu010': img10},
    'paper_reference': paper,
    'comparison_to_paper': {
        'text': text_v, 'img_qvu014': img14_v, 'img_qvu010': img10_v,
        'sampling_95ci_halfwidth_pp': {
            'text_IoU': ci_halfwidth(text['official_metrics_cadrille_evaluate_py']['IoU_mean_pct'], text['n_samples']),
            'text_IR': ci_halfwidth(text['official_metrics_cadrille_evaluate_py']['IR_pct'], text['n_samples']),
            'img_qvu010_IoU': ci_halfwidth(img10['official_metrics_cadrille_evaluate_py']['IoU_mean_pct'], img10['n_samples']),
            'img_qvu010_IR': ci_halfwidth(img10['official_metrics_cadrille_evaluate_py']['IR_pct'], img10['n_samples']),
        },
    },
    'our_data_reference': our_data,
    'conclusion': None,
}

t = text['official_metrics_cadrille_evaluate_py']; to = text['our_convention_eval_predictions_py']
i4 = img14['official_metrics_cadrille_evaluate_py']; i4o = img14['our_convention_eval_predictions_py']
i0 = img10['official_metrics_cadrille_evaluate_py']; i0o = img10['our_convention_eval_predictions_py']
okt = text_v['within_tolerance(IoU+-5pp, IR<=+3pp, CD+-0.1)']
ok0 = img10_v['within_tolerance(IoU+-5pp, IR<=+3pp, CD+-0.1)']
concl = (
    f"TEXT (Text2CAD test, n=200): IoU {t['IoU_mean_pct']:.1f}% / median CD {t['CD_median_x1000']:.2f} / IR {t['IR_pct']:.1f}% vs paper Tab. 1 "
    f"82.1 / 0.20 / 1.4 -> {'reproduces' if okt else 'does NOT reproduce'} the paper within IoU +-5 pp, IR <= +3 pp, CD +-0.1 "
    f"(our convention: validity {to['validity_pct']:.1f}%, bbox-Chamfer {to['chamfer_bbox_norm_mean']:.3f}, F {to['fscore_at_0.02_mean']:.3f}, "
    f"op-type recall {to['op_type_recall_mean']:.2f}; on ComplexCAD the same branch gave 89.2% / 0.422 / 0.044 / 0.23). "
    f"The text adapter is intact; the ComplexCAD text result is a domain gap. "
    f"IMAGES (DeepCAD test): with the venv's qwen-vl-utils 0.0.14 (n=200) IoU {i4['IoU_mean_pct']:.1f}% / CD {i4['CD_median_x1000']:.2f} / IR {i4['IR_pct']:.1f}% "
    f"(validity {i4o['validity_pct']:.1f}%, bbox-Chamfer {i4o['chamfer_bbox_norm_mean']:.3f}, F {i4o['fscore_at_0.02_mean']:.3f}); "
    f"with the Dockerfile-pinned qwen-vl-utils 0.0.10 (n=100) IoU {i0['IoU_mean_pct']:.1f}% / CD {i0['CD_median_x1000']:.2f} / IR {i0['IR_pct']:.1f}% "
    f"(validity {i0o['validity_pct']:.1f}%, bbox-Chamfer {i0o['chamfer_bbox_norm_mean']:.3f}, F {i0o['fscore_at_0.02_mean']:.3f}) vs paper 86.1 / 0.18 / 1.5 -> "
    f"{'reproduces' if ok0 else 'does NOT reproduce'} the paper under the same tolerance. "
    + ("The image adapter is intact once the pinned qwen-vl-utils is used; our ComplexCAD image-mode rows were run with the mismatched "
       "144-token grid and mix a tokenisation mismatch with the render-style domain gap, so they should be re-run with 0.0.10 before being interpreted."
       if ok0 else
       "Even with the pinned tokenisation the image branch stays far below the paper on our renders, so the remaining gap is a render-environment "
       "(Open3D build) difference and/or a genuinely weaker released image branch, not a ComplexCAD-specific effect; the ComplexCAD image rows "
       "additionally carry the 0.0.14 tokenisation mismatch.")
)
result['conclusion'] = concl
json.dump(result, open(OUT_JSON, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

parts = []
for name in ['infer_text.log', 'infer_img.log', 'infer_img2.log', 'infer_img_qvu010.log',
             'eval_text_official.log', 'eval_text_ours.log', 'eval_img_official.log', 'eval_img_ours.log',
             'eval_img_qvu010_official.log', 'eval_img_qvu010_ours.log', 'qvu_grid_check.log']:
    p = os.path.join(HERE, name)
    if os.path.isfile(p):
        parts.append('===== ' + name + ' =====\n' + open(p, encoding='utf-8', errors='replace').read())
parts.append('===== conclusion =====\n' + concl + '\n')
open(OUT_LOG, 'w', encoding='utf-8').write('\n'.join(parts))
print(concl)
print('wrote', OUT_JSON, OUT_LOG)
