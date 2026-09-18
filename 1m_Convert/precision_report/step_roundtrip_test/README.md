# CadQuery → STEP 精度往返核查 (Round-trip Precision Test)

> 任务4 精度评估的支撑实验之一：验证本数据集「参数 → CadQuery 几何 → STEP 文件」的精度链路是否无损。

## 实验目的

验证：cadquery.py 源码里的（含小数）尺寸参数，经 CadQuery 执行并导出为 STEP 文件后，
STEP 文件中的实际几何尺寸与源码几何是否一致——即**精度链路是否端到端无损**。

这与「量化损失实验」(`../quantization_loss.py`) 形成对照：DeepCAD/CAD-Recode 在**数据表示层**
就有损（256 级量化 / 0.5mm 网格），而本数据集在表示层无量化，需进一步验证下游导出也无损。

## 方法

对 `cases/` 下每个样例：
1. 执行 `cadquery.py` 得到源码几何，量其 bounding box；
2. 载入同目录 `model.step`，重新量 bounding box；
3. 对比两者差值（STEP 往返误差）；
4. 检查 STEP 文件内坐标保留的有效数字位数。

## 结论

**CadQuery → STEP 转换本质无损**，往返误差在 64 位浮点机器精度量级：

| 样例 | 关键参数 | 源码几何 bbox | STEP 载入 bbox | 往返误差 |
|---|---|---|---|---|
| 0310bb67 | boss_fillet = 0.75 | 80.000000 | 80.000000 | **1.08×10⁻¹³ mm** |
| 0a4c4de1 | scale_factor = 0.85 → 派生 78.249641 | 78.249641 | 78.249641 | **1.71×10⁻¹³ mm** |
| 071a220d | tolerance = 0.01 → 派生 98.994949 | 98.994949 | 98.994949 | **6.54×10⁻¹³ mm** |

要点：
1. **往返误差最大 6.5×10⁻¹³ mm**（约 0.00000000000065 mm）——这是双精度浮点舍入极限，工程上等同零误差。
2. **STEP 用科学计数法保留 12–13 位有效数字**（如 `-9.478148308906E-02`），源码写多精密就存多精密，不舍入。
3. **派生参数可产生高精度真实尺寸**：源码命名参数虽写 `0.85`，经 `scale_factor × 尺寸` 计算后实际几何尺寸为 `78.249641 mm`（6 位精度），STEP 完整保留。

> 即：本数据集的精度优势不在「写了几位小数」，而在**表示层无量化 + 派生参数可算出任意精度真实尺寸 + 全链路（参数→几何→STEP）无损保留**。相比之下 DeepCAD/CAD-Recode 的精度损失发生在表示层，无法通过下游导出挽回。

## 文件清单

```
step_roundtrip_test/
├── README.md                  本说明
├── step_roundtrip_test.py     测试脚本(自包含, python -X utf8 step_roundtrip_test.py)
├── results.txt                上次运行的完整输出
└── cases/                     3 个被测样例(从 output/ 复制)
    ├── 0310bb67-.../          cadquery.py + model.step  (boss_fillet=0.75)
    ├── 0a4c4de1-.../          cadquery.py + model.step  (scale_factor=0.85)
    └── 071a220d-.../          cadquery.py + model.step  (tolerance=0.01)
```

## 复现

```bash
cd step_roundtrip_test
python -X utf8 step_roundtrip_test.py
```
依赖 cadquery（与生成数据集相同的 Python 环境）。
