# Third-party code and data

The MIT licence in `LICENSE` covers the code written for the thesis. The items
below keep their own licences. Each directory ships the upstream licence file
unchanged.

## Inherited data: Zero-To-CAD

The 10,000 base programs, the STL and STEP exports and the eight rendered views
per model come from the test split of the Zero-To-CAD corpus.

| | |
|---|---|
| Source | https://huggingface.co/datasets/ADSKAILab/Zero-To-CAD-1m (revision `09dbd180`, `test` split) |
| Authors | M. Ataei, F. Askari, K. Rahimi Malekshan, P. K. Jayaraman (Autodesk Research) |
| Paper | Zero-to-CAD: Agentic Synthesis of Interpretable CAD Programs at Million-Scale Without Real Data, arXiv:2604.24479, 2026 |
| Licence | Apache License 2.0, full text in `LICENSES/Apache-2.0.txt` |

This repository contains no upstream program files. The inherited files are
redistributed only inside the dataset record on Zenodo, under Apache 2.0 with
this attribution. The modalities added by the thesis are released under
CC BY 4.0.

The inference script `z2c_repro/run_zero2cad.py` loads the upstream model
`ADSKAILab/Zero-To-CAD-Qwen3-VL-2B` from Hugging Face. The model weights are not
included here.

## Reconstruction baselines

Each directory is a clone of the upstream repository at the commit below. The
thesis added run scripts and, where listed, modified upstream files. All files in
a directory, including the additions and modifications, are distributed under
that directory's upstream licence. The exact modifications are in
`third_party_patches/`.

| Directory | Upstream | Commit | Licence | Modified upstream files | Added by the thesis |
|---|---|---|---|---|---|
| `cadrille_repro/` | https://github.com/col14m/cadrille | `338db11` | Apache 2.0 | `cadrille.py`, `dataset.py` | `run_cadrille.py`, `train_closed_loop.py`, `train_closed_loop_utils.py`, `train_complexcad.py`, batch files |
| `cadrecode_repro/` | https://github.com/filaPro/cad-recode | `03e3262` | CC BY-NC 4.0 | none | `run_cadrecode.py` |
| `cadfit_repro/` | https://github.com/ghadinehme/CADFit | `fb31f63` | CC BY-NC 4.0 | `cadquery_ops.py`, `greedy_search.py` | `exec_cc.py`, `prep_batch.py`, `prep_one.py`, `prep_real.py` |

CC BY-NC 4.0 forbids commercial use of `cadrecode_repro/` and `cadfit_repro/`.
The rest of the repository has no such restriction.

The model checkpoints of these methods are downloaded from their upstream
locations at run time and are not included.

## GrabCAD meshes

The real-part spot check uses community meshes from GrabCAD. They are used under
the GrabCAD Terms of Use and are **not** redistributed.
`_review/grabcad_manifest.csv` lists the model page, file identifier, MD5 and
processing of every mesh so that they can be downloaded again.

## Python dependencies

CadQuery, OCP/OpenCASCADE, cq_warehouse, trimesh, ezdxf, PyTorch, Transformers,
PEFT and the other packages pinned in `env/` are installed from their usual
package indexes under their own licences and are not vendored.
