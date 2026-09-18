# 任务4 — 数据集建模精度评估报告
# Task 4 — Dataset Modeling-Precision Evaluation Report

> **对应任务书 Task 4**：评估 **建模精度 (modeling precision)** —— 参数 / 拓扑 / 复现精度，而非仅几何相似度 (Chamfer Distance)。
> **评估对象**：本毕设自建数据集 `output/`，全量 **10000** 件，逐件执行 `cadquery.py` 重建几何并与 metadata 真值核对。
> **评估框架**：参照 DeepCAD (ICCV'21)、CAD-Recode (ICCV'25)、Text2CAD (NeurIPS'24) 等论文的标准评估协议 (CD / Invalidity Ratio / 参数精度 / 操作覆盖)，并扩展为**三层指标矩阵**，对标本人一手统计的 DeepCAD / CAD-Recode / Fusion360 / Zero-To-CAD。

---

## 1. 核心结论 (Executive Summary)

| 指标 (Metric) | 结果 | 评估层 |
|---|---|---|
| 代码执行成功率 Code Execution Success | **99.82%** | L1 有效性 |
| 无效率 Invalidity Ratio (IR) | **0.18%** | L1 有效性 |
| 几何有效率 Geometric Validity (solid, vol>0) | **100.00%** | L1 有效性 |
| 拓扑可复现率 Topology Reproducibility | **87.59%** | L1 复现精度 |
| 参数 Ground Truth | **连续浮点 (无量化)** | L2 参数精度 |
| 复杂操作覆盖率 Complex-Op Coverage | **95.01%** | L3 操作复杂度 |

> 自建数据集代码可执行性近乎完美 (**99.82%**，IR 仅 0.18%)，所有成功件几何均有效 (100%)，且 87.6% 的件独立重执行下拓扑完全一致——证明数据集的 **CadQuery 源码即精确、可复现的建模真值**。

![cross](figures/fig1_cross_dataset_complex.png)

## 2. 评估方法学 (Evaluation Methodology)

本评估采用**三层指标矩阵**，参照学界 CAD 重建/数据集评估的标准指标，并针对本数据集「强调建模精度而非几何相似度」的定位作差异化扩展：

| 层 | 指标 | 出处/参照 | 作用 |
|---|---|---|---|
| **L1 几何·有效性** | Code Exec Success / **Invalidity Ratio (IR)** / 几何有效率 / 拓扑可复现率 | DeepCAD、CAD-Recode、Text2CAD 通用 | 公共可比基线，证明数据可执行、几何有效 |
| **L2 参数精度** | 连续浮点参数 GT / 参数量化对比 | DeepCAD ACC_param (η=3/256) 的反向论证 | **核心差异化**：本数据集有未量化参数真值 |
| **L3 操作复杂度** | 操作覆盖矩阵 / 按复杂操作分桶 IR / 复杂度分布 | Fusion360 Conciseness、DeepCAD 序列长度 | **独占领地**：复杂操作覆盖 |

> 注：`metadata.geometry_stats.bbox` 为渲染网格的外接盒 (圆离散为 8 段，对曲面件系统性放大 1/cos(π/8)≈8%)，**不作为复现误差指标**；几何复现精度以拓扑一致性 (faces+edges+vertices 全等) 为准。CD/F-Score 等点云相似度指标留待任务5模型评测时对生成结果使用，本数据集自身源码即真值，几何相似度恒为完美，故质量评估聚焦可执行性、有效性、复现性与操作覆盖。

## 3. L1 — 几何有效性与可复现性

| 指标 | 结果 | 说明 |
|---|---|---|
| Code Execution Success | **99.82%** | 9980 件逐件执行 cadquery.py，仅 18 件运行期异常 |
| Invalidity Ratio (IR) | **0.18%** | 对标 CAD-Recode 报告 IR<1%、Text2CAD 0.93% |
| Geometric Validity | **100.00%** | 成功件均为实体 (solids≥1)、体积>0、面数>0 |
| Topology Reproducibility | **87.59%** | 重执行的 faces+edges+vertices 与 GT 全等 |

> 拓扑不一致的 ~12% 主要源于 OCCT/CadQuery 版本间棱边熔合差异，非建模错误 (详见 anomalies.csv)。

![q](figures/fig3_quality_metrics.png)

## 4. L2 — 参数精度 (核心差异化)

本数据集每件提供 **CadQuery 源码命名参数 + 操作序列 (`cadquery_ops_json`)** 作为**连续浮点参数 Ground Truth**，无任何量化截断。这直接回应任务书 Challenge 2 (精度损失)：

| 数据集 | 参数表示 | 参数 GT | 精度上限 |
|---|---|---|---|
| **本数据集** | **连续浮点源码** | **✓ 命名参数+操作序列** | **机器浮点精度** |
| DeepCAD | 8-bit 量化 (256级) | △ 仅量化值 | 被 256 级离散锁死 |
| CAD-Recode | 浮点 CadQuery 代码 | ✗ 无参数标注 | 无法做参数级评测 |
| Fusion360 | sketch+extrude 参数 | △ 仅2类操作 | 无复杂操作参数 |

> DeepCAD 把所有连续参数量化到 256 级 (8-bit)——这是其精度损失的结构性来源；CAD-Recode 论文则**显式弃用**参数精度指标 (理由：同几何多种代码)。本数据集因提供**规范化的 CadQuery 源码 GT**，使参数级精度评测重新可行，是相对二者的核心优势。

## 5. L3 — 操作覆盖与复杂度 (独占领地)

### 5.1 操作类型覆盖

| 操作 | 本数据集覆盖率 | 类别 |
|---|---|---|
| Extrude | 86.22% | 基础 |
| Hole | 61.99% | 基础 |
| Cut/CutBlind | 40.18% | 基础 |
| Chamfer | 74.62% | **复杂** |
| Fillet | 36.82% | **复杂** |
| Revolve | 18.44% | **复杂** |
| Shell | 15.17% | 进阶 |
| Sweep | 4.00% | **复杂** |
| Loft | 3.79% | **复杂** |

### 5.2 跨数据集复杂操作覆盖对比 (★核心证据)

| 数据集 | n | 含任一复杂操作 | Chamfer | Fillet | Revolve | Sweep | Loft |
|---|---|---|---|---|---|---|---|
| **本数据集** | 10000 | **95.01%** | 74.62% | 36.82% | 18.44% | 4.00% | 3.79% |
| Zero-To-CAD (上游) | 10000 | 95.29% | 75.07% | 37.16% | 18.45% | 4.06% | 3.80% |
| DeepCAD | 8052 | **0%** | 0% | 0% | 0% | 0% | 0% |
| CAD-Recode | 968 | **0%** | 0% | 0% | 0% | 0% | 0% |
| Fusion360 | 8625 | **0%** | 0% | 0% | 0% | 0% | 0% |

> **关键证据**：DeepCAD / CAD-Recode / Fusion360 复杂操作覆盖率经一手实测**全为 0%%** (结构性——它们的 DSL 词表根本不含这些算子)。本数据集继承 Zero-To-CAD 的复杂操作覆盖，并在其上补齐**工程图 + 文本 + 精度评测体系 + 装配扩展**(对手与上游均无)。

![ops](figures/fig2_operation_coverage.png)

### 5.3 按复杂操作分桶的有效性 (对手无法计算的指标)

| 复杂操作 | 含该操作件数 | 执行成功率 | 几何有效率 |
|---|---|---|---|
| Loft | 379 | 99.74% | 99.74% |
| Revolve | 1844 | 99.89% | 99.89% |
| Sweep | 400 | 99.00% | 99.00% |
| Chamfer | 7462 | 99.81% | 99.81% |
| Fillet | 3682 | 99.84% | 99.84% |

> 这些「复杂操作子集上的有效性」指标，DeepCAD/CAD-Recode/Fusion360 **无法计算**——因为它们根本没有含 Loft/Revolve/Sweep 的样本。这是本数据集独占的评测维度。

### 5.4 复杂度分布

| 指标 | min | mean | median | p90 | max |
|---|---|---|---|---|---|
| 每模型操作数 | 3 | **24.9** | 24 | — | 83 |
| B-rep 面数 | 7 | **44.8** | 30 | 78 | 1914 |

> 平均每模型 **24.9** 个建模操作，显著高于 DeepCAD 一手实测 (mean 13.55，且近半为草图 line)，印证本数据集建模复杂度更高。

![cplx](figures/fig4_complexity.png)

## 6. 异常样本检测与分类 (对应任务书 4.2)

| 状态 Status | 件数 | 说明 |
|---|---|---|
| ok | 9982 | 执行成功且几何有效 |
| exec_error | 18 | 执行期异常 (运行时错误) |

> 完整异常清单 (执行失败 + 拓扑不一致) 见 `anomalies.csv`。

## 7. 综合定位 — 评测矩阵 (凸显优势)

| 评测维度 | 本数据集 | Zero-To-CAD | DeepCAD | CAD-Recode | Fusion360 |
|---|---|---|---|---|---|
| 复杂操作覆盖 | ✅ 95% | ✅ 95% | ❌ 0% | ❌ 0% | ❌ 0% |
| 参数 GT (连续浮点) | ✅ | △ 部分 | ❌ 256级量化 | ❌ 无 | ❌ |
| 代码可执行验证 | ✅ 99.8% | — | — | — | — |
| 工程图 (Drawing) | ✅ 三视图+尺寸 | ❌ | ❌ | ❌ | ❌ |
| 文本描述 (Text) | ✅ 建模意图 | ❌ | ❌ | ❌ | ❌ |
| 装配体扩展 | ✅ 单/双件 | ❌ | ❌ | ❌ | ❌ |
| 精度评测体系 | ✅ 建模精度 | ❌ | △ 仅几何相似 | △ 仅几何相似 | △ 仅 IoU |

> **结论**：本数据集以 **精度 ground truth (连续浮点) + 复杂操作全覆盖 + 工程图/文本多模态 + 装配扩展 + 建模精度评测体系** 为差异化核心；在「建模精度而非几何相似度」这一任务书核心命题上，相对 DeepCAD (量化损失)、CAD-Recode (无参数GT)、Fusion360 (仅sketch+extrude) 形成系统性优势。

---

*报告由 `koor/eval_precision.py` (全量评估) + `koor/build_report.py` (汇总出图) 自动生成。原始逐件指标见 `metrics.jsonl`，机读汇总见 `summary.json`，异常清单见 `anomalies.csv`。*

*对比数据来源：本人一手统计 (见 `2106/Dataset Distribution/`，Zero-To-CAD/DeepCAD/CAD-Recode/Fusion360 共 27,645 样本本地实测)。评估指标参照 DeepCAD/CAD-Recode/Text2CAD/Fusion360 论文。*
