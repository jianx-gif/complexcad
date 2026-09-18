# 归一化（量化）数据集 生成转换管线

把 Zero-To-CAD CadQuery 模型的尺寸**量化到 [1,10000] 整数坐标网格**，并按需
产出与原始数据集同构的**全模态**（量化代码 + STEP/STL/BREP + 工程图 + 点云 +
文本 + koor 元数据）。用于点云→CAD 网络的**精度导向训练标签**。

## 依赖

本管线依赖外层工程图核心脚本（位于本目录的上一级 `data/`）：
`match.py · make_drawings.py · projlib.py · drawing.py · annotate.py ·
params.py · iso_knowledge.py · augment_data.py`
脚本通过 `sys.path.insert(0, ROOT)` 自动引入，运行时需保证本目录在
`data/1m_Convert/` 下、上述脚本在 `data/`。
外部库：`cadquery / OCP · pyarrow · numpy · trimesh · matplotlib · huggingface_hub`。

## 核心转换链（按数据流）

| 脚本 | 作用 | 输入 → 输出 |
|------|------|------|
| **koor_transform.py** | 核心：AST 语义缩放。长度×scale 取整，角度/个数/比例不变 | 源码字符串 → 量化源码 |
| **bbox_persistent.py** | 常驻 worker：import cadquery 一次，反复执行返回包围盒 | stdin{code} → stdout{bb} |
| **convert_fast.py** | 单模型逻辑：原始bbox→定scale→缩放→缩放后bbox→两步验证→平移；本地100k驱动 | parquet → test.parquet + dropped.jsonl |
| **convert_1m.py** | 1M 主驱动：流式读 HF、worker 池、每源文件出 parquet、断点续传 | HF parquet → koor_1m/<split>/*.parquet |
| **recover_1m.py** | 恢复 pass：长超时90s + min_mag=1 救回首轮失败项 | dropped.jsonl → *.rec.parquet |

## 落地与全模态生成

| 脚本 | 作用 |
|------|------|
| **extract_converted_py.py** | 把转换后量化代码按 uuid 提取成 `converted_py/<uuid>/cadquery.py` + koor.json |
| **build_koor_geometry.py** | 对量化代码走完整管线一步到位出 13 模态 → `koor_geometry/<uuid>/`。含量化专用设置：剖视阈值 2.5、整数网格吸附、内部标注加强 |
| **augment_koor.py** | 给已生成的量化件批量补三模态（点云/brep/文本），可续传 |
| **export_to_output.py** | 把转换件按原始代码落地到 output/ 布局（复用 parquet 已有模态） |

## 校验与分析

| 脚本 | 作用 |
|------|------|
| **verify_fast.py** | 抽样执行 cadquery_file 校验几何落在 [1,10000] |
| **verify_recover.py** | 验证量化代码可无损还原：执行→÷scale→对比原始（误差应 ≤1/scale） |
| **_digit_stats.py** | 数值末位分布分析（逐位 token 偏置） |
| **peek_1m.py / viz_koor.py** | 进度抽样 / 原始-转换对比图渲染 |

## 量化专用设计（在 build_koor_geometry.py 内，仅影响量化管线）

- **整数网格吸附**：`match._SNAP_GRID=scale` + `_SNAP_INT_DISPLAY`，量化工程图
  标注吸附回整毫米（299.47→300），大件(非整scale)也显示整数。
- **剖视阈值降到 2.5**：`md.SECTION_RATIO=2.5`，有内部结构的件多触发 A-A 全剖
  （实测约 33% 件触发）。
- **内部标注加强**：`_WALL_MAX_NEW=8 / _SECTION_MAX=10 / _LOC_MAX=8`。
  > 以上均为运行时覆盖，`match.py` 默认值不变，正式 output/ 工程图不受影响。

## 关键参数

- scale = `min(100, 9990/最长边mm)`：≤100mm 件用 100（0.01mm 网格），大件自适应
- 盒子 [1,10000]，每件存自己的 scale + 平移 offs，÷scale 精确还原
- 落盒率 100%，保留率约 85% + 恢复救回约 20%

## 已知问题

见 **QUANTIZATION_DIGIT_BIAS.md**：固定 ×100 使数值末位偏 0（59.7%），在逐位
token 模型下低位数字饥饿。修法方案待与导师对齐。

## 典型用法

```bash
# 1) 全量转换 1M（或本地子集 convert_fast）
python convert_1m.py --split test --workers 16 --timeout 25
python recover_1m.py --dir <koor_dir>          # 救回失败项

# 2) 提取量化代码
python extract_converted_py.py

# 3) 对量化代码出全模态
python build_koor_geometry.py <uuid> ...        # 单件
python build_koor_geometry.py --all 100         # 前 N 件
python augment_koor.py                          # 给已有件补三模态

# 4) 校验
python verify_recover.py                        # 量化无损还原验证
python verify_fast.py <parquet> 800 12          # 落盒抽检
```

## Installation and CLI（安装与命令行）

本目录是一个可安装的 Python 包 **`complexcad-koor`**（`pyproject.toml`，setuptools，
MIT，Python ≥ 3.10）。安装后得到包 `koor`（即本目录 `koor/`）和命令 **`koor`**。
**文件一个都没有移动**：外层核心模块（`match / make_drawings / augment_data /
params / iso_knowledge / drawing / projlib / annotate`）仍在 `data/` 根目录，
在 `pyproject.toml` 里以 `py-modules`（`package-dir "" = ".."`）声明；
`koor/` 下各脚本仍可像以前一样直接 `python koor/xxx.py` 运行，逻辑未改。
唯一改动：`augment_koor.py / export_to_output.py / build_koor_geometry.py` 里的
`sys.path.insert(0, ROOT)` 改为仅在包**未安装**时执行
（`if importlib.util.find_spec("match") is None:`），装好包后不再操作 `sys.path`。

```bash
# 安装(可编辑模式, 在 cadfit-env 里)
cd E:\3005\data\1m_Convert
python -m pip install -e .                 # 离线: 加 --no-build-isolation --no-deps
python -m pip install -e ".[geometry,convert,test]"   # 可选: 几何/1M转换/测试依赖

# 命令行 (每个子命令 = 原脚本, 参数原样透传)
koor --help                                # 列出全部子命令
koor eval-precision --help                 # 脚本自己的 argparse 帮助
koor augment 50            # == python koor/augment_koor.py 50
koor export 20             # == python koor/export_to_output.py 20
koor geometry --all 100    # == python koor/build_koor_geometry.py --all 100
koor eval-precision --jobs 8 --resume
koor eval-predictions --self-test --limit 30
koor retrieval --jobs 8
koor quantization --levels 256
koor score cadrecode predictions/test_subset.txt --jobs 2
koor transform < part.py   # koor_transform 单文件量化
koor config                # 打印生效配置
python -m koor ...         # 等价写法

# 单元测试 (不需要 1 万件数据, < 1 min)
python -m pytest tests -q
```

**配置文件**：可选 `koor.toml`（模板见 `koor.example.toml`；查找顺序
`--config PATH` → `$KOOR_CONFIG` → `./koor.toml` → `1m_Convert/koor.toml`），
环境变量 `KOOR_ROOT / KOOR_OUTPUT_DIR / KOOR_SPLITS_DIR / KOOR_PREDICTIONS_DIR /
KOOR_REPORT_DIR / KOOR_NAMES_FILE / KOOR_CONVERT_OUTDIR / KOOR_CONVERT_TRAIN_DIR /
KOOR_LOG_LEVEL / KOOR_LOG_FILE` 优先于文件。脚本本身不读配置、默认值不变；
CLI 只把**显式设置**的键转发给脚本**已有**的路径参数
（`eval-predictions/adapt-cadrecode --names-file`、`convert --outdir`、
`recover/peek --dir`），命令行给了该参数则以命令行为准。没有配置文件时
`koor <cmd> ...` 与 `python koor/<script>.py ...` 行为完全一致。

**日志**：`koor/logging_setup.py` 的 `setup_logging(level, logfile)` 只给 CLI 层
用（记录跑了哪个脚本、参数、配置来源、耗时、退出码；stderr + 可选文件
`--log-file` / `KOOR_LOG_FILE`）。脚本内部原有 `print` 输出保持不变。
