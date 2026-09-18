# ComplexCAD release — file manifest

Paths are relative to the release root. `checksums.txt` lists the SHA-256 of every split,
environment and result file named below. The thesis sources (`_rev_clone/`) are not part of
the data release.

## Environments

| Path | Purpose |
|---|---|
| `env/environment-cadfit.yml` | pipeline and evaluation (CadQuery 2.6.1, OCP 7.8.1, trimesh 4.11.5, ezdxf 1.4.4) |
| `env/environment-cadquery.yml` | audit scripts (CadQuery 2.7.dev, OCP 7.8.1) |
| `env/requirements-training.txt` | closed-loop training venv (Python 3.13, PyTorch 2.6.0 + CUDA 12.4, Transformers 4.50.3, PEFT 0.20.0) |

## Data

| Path | Content |
|---|---|
| `test/*.parquet` | upstream Zero-To-CAD test split (24 files, 10000 programs; not redistributed) |
| `output/<uuid>/` | one directory per part (10000, the complete upstream test split): `cadquery.py`, `model.step`, `model.stl` (inherited), `model.brep`, `image_0..7.png` (inherited), `point_cloud.npy/.ply`, `metadata.json`, `description.json/.txt`, `drawing.png/.svg/.dxf` |
| `1m_Convert/assemblies_slim/` | 1005 single-fastener assemblies |
| `1m_Convert/two_part_assemblies_slim/` | 693 two-part assemblies |
| `splits/` | `test_400.txt`, `val_100.txt`, `train.txt`, `quarantine_near_duplicates.txt`, `quarantine_pairs.json`, `non_executing_18.txt`, `splits.json`, `assemblies.json`, `assembly_loop_test.txt` (train 9212, val 100, test 400, quarantine 271; 20 programs missing until 2026-09-13 were restored on that date and are in no training arm and no seeded audit sample; `_review/_restore20/`) |
| `predictions/<method>/` | predicted programs of every evaluated method and training arm; the closed-loop arms are the post-restoration runs (`cadrille_cc`, `cadrille_ctrl`, `cadrille_cc_text`, `cadrille_cc_draw`), plus `cadrille_cc_r2` (random sample order) and `cadrille_cc_run1_reinfer` (the pre-restoration adapter re-inferred); the pre-restoration runs are kept under `_review/_pre10000/predictions/` |
| `_review/grabcad_manifest.csv`, `real_root/real_metrics.json`, `real_root/predictions/`, `real_root/pred_stl/` | GrabCAD spot check: manifest (model page, file id, MD5, size, processing) and the scores and reconstructions; the 26 downloaded meshes themselves (`real_root/output/`, `cadfit_repro/grabcad_in/`) are used under the GrabCAD Terms of Use and are **not** part of the public release |

## Code

| Path | Role |
|---|---|
| `augment_data.py` | point cloud, B-rep, metadata, text description per part (`augment_data.py [start] [count]`) |
| `make_drawings.py`, `drawing.py`, `projlib.py`, `match.py`, `annotate.py`, `params.py`, `iso_knowledge.py`, `regen_all.py` | engineering-drawing chain |
| `1m_Convert/produce_one.py`, `batch_assemble.py`, `assemble_fasteners.py`, `assemble_two.py`, `dataset_source.py` | assembly chain; `dataset_source.py` reads `Z2C_PARQUET_GLOB` |
| `1m_Convert/koor/eval_precision.py`, `eval_predictions.py`, `quantization_loss.py` | quality metrics and prediction scoring (output `1m_Convert/precision_report/`) |
| `Dataset Distribution/scripts/stat_*.py` | first-hand survey of the four existing datasets (Chapter 3) |
| `cadrille_repro/train_closed_loop.py` (`--sampler bucket|random`), `run_cadrille.py`, `run_all10k.bat`, `run_c2.bat` | closed-loop training and inference; the two batch files are the serial GPU chains of the 10000-corpus re-run |
| `_review/exp_*.py`, `make_*.py` | every experiment and table of Chapters 4–6 (see below) |

## Results (`_review/`, `1m_Convert/precision_report/`)

| File | Thesis item |
|---|---|
| `precision_report/metrics.jsonl` | L1 metrics per model (execution, validity, entity counts) |
| `precision_report/pred_metrics_<method>.jsonl` | scored predictions (Chapter 6 tables) |
| `precision_report/quantization_loss.json` | simulated quantisation (Chapter 5, quantisation table) |
| `exp_g_measurers.json`, `exp_w_revolve.json` | per-operation measurers |
| `exp_v_brepcheck.json`, `exp_v2_brepcheck_detail.json`, `brepcheck_invalid.json` | kernel validity, failure classes, tolerances, 61 invalid UUIDs |
| `exp_x_adjacency.json`, `exp_y_step_roundtrip.json`, `exp_z_tessellation.json` | adjacency, STEP round trip, mesh deviation |
| `exp_d_point_ablation.json`, `exp_d2_chamfer_coverage.json`, `exp_d3_low_n_coverage.json` | point-count ablation |
| `exp_t_drawing_audit.json`, `exp_u_dim_correctness.json`, `exp_ee_linetype_audit.json`, `exp_gg_hlr_fragments.json`, `exp_aa_drawing_determinism.json` | drawing audits |
| `exp_c2_text_audit_sample200.json` | automated operation check restricted to the 200 human-audited descriptions (Sec. 4.5) |
| `exp_c_text_audit.json`, `text_audit/result_text_audit.json` (+ `text_audit/checklist.csv`, reviewer CX) | text description audit (automated; human, 200 descriptions) |
| `predictions/cadrille_img_qvu010/`, `predictions/cadrille_img_text_qvu010/` (+ `precision_report/pred_metrics_*_qvu010.jsonl`) | released checkpoint, image and image+text modes on the 400-model subset re-run with qwen-vl-utils 0.0.10 (Table 6.8); the original `cadrille_img`, `cadrille_img_text` folders (0.0.14 grid) are kept as the tokenisation-mismatch comparison |
| `_review/cc_draw_lora_qvu010/`, `predictions/cadrille_cc_draw_qvu010/` (+ `precision_report/pred_metrics_cadrille_cc_draw_qvu010.jsonl`) | drawing arm retrained with qwen-vl-utils 0.0.10 (the image grid of the released checkpoint); the earlier 0.0.14 run `cc_draw_lora` / `cadrille_cc_draw` is kept as comparison (Table 6.12) |
| `exp_i2_retrieval_noquarantine.json`, `predictions/retrieval_noq/` | retrieval baseline with the 271 quarantined near-duplicates removed from the pool (Sec. 6.2) |
| `exp_hh_adapter_sanity.json`, `exp_hh_adapter_sanity.log`, `_hh_adapter/` | released cadrille text/image branches on their official test data (Text2CAD, DeepCAD renders); qwen-vl-utils 0.0.14 vs 0.0.10 token-grid finding (Sec. 6.2) |
| `exp_w3_loft_sweep.json`, `exp_w3_loft_sweep_records.jsonl` | loft-section and sweep-path measurers on all loft and sweep calls, feature body and released B-rep (Table 5.8) |
| `exp_w2_revolve_axis.json`, `exp_w2_revolve_axis_records.jsonl` | revolve-axis measurer: declared vs. measured axis for 1767 statically resolvable revolve calls (Table 5.8 rows, Sec. 5.2) |
| `exp_ii_quant_by_class_pos.json` | simulated quantisation loss per class with a separate position/offset/spacing class (Table 5.7) |
| `grabcad_provenance_table.json`, `grabcad_provenance_table.tex` | per-mesh provenance of the five GrabCAD spot-check meshes: raw/used MD5, faces before/after, pymeshlab recipe (Table G.1) |
| `_verify0917/` | 2026-09-17 one-by-one verification of the 237 supervisor annotations: items, verdicts with evidence, fixes applied |
| `drawing_audit/result_double_review.json` (+ `checklist_A.csv`, `checklist_B_zh.csv`) | two-reviewer drawing audit, 200 sheets |
| `exp_j_perop_prf.json`, `exp_j_strict.json`, `exp_q_param_error.json`, `exp_q_mae.json`, `exp_s_precision2.json`, `exp_bb_loop_significance.json` | closed-loop tables and significance (post-restoration runs; `_restore20/analyze_diag.json` = repetition-loop diagnosis) |
| `exp_r_asm.json` | assembly closed loop |
| `exp_cc_param_dedup.json`, `exp_dd_excluded20.json`, `exp_ff_param_by_operation.json`, `param_ranges.json` | split checks, the 20 restored programs (their re-execution record), parameter tables |

## Logs

`_review/*.log` (67 files) record every training, inference, evaluation and audit run,
including the training-loss curves in `_review/cc_*_lora/log.txt`.

## Restoration of 2026-09-13

`_review/_restore20/` holds the scripts and logs of the restoration: `extract20.py` (parquet rows -> part folders), `augment20.py` + `desc_0607.py` (derived modalities with the release's description code, validated byte for byte on the other 9980 parts by `validate_desc_0607.py`), `draw20.py` (drawings), `restored_uuids.txt`, and the pre-restoration result files under `_review/_pre10000/`.


## Installable package (2026-09-17)

`1m_Convert/pyproject.toml` installs the toolchain as `complexcad-koor` 1.0.0 (`pip install -e 1m_Convert`): `koor` CLI with 18 sub-commands dispatching to the unchanged scripts, TOML configuration (`koor.example.toml`) with `KOOR_*` overrides, per-invocation logging, `1m_Convert/tests/` (62 pytest tests, ~3 s, no dataset needed). Scripts remain runnable from the checkout; the only code change is a two-line import guard in `augment_koor.py`, `export_to_output.py`, `build_koor_geometry.py`. `augment_data.py` seeds the point sampler per model UUID since 2026-09-17 (released clouds predate this).
