# Zero-To-CAD 坐标量化 — 交接文档

把 Zero-To-CAD 的 CadQuery 代码，参数缩放并平移进 **[1,10000]³ 整数坐标盒子**，
供 point-cloud→CAD 训练用（÷10000→[0,1] 喂网络，后处理 ×scale 还原绝对尺寸）。

---

## 1. 方案（已定稿）

- **固定 scale=100**（1 单位 = 0.01mm）：`s = min(100, 9990/最长边mm)`
  - ≤100mm 的模型 → scale=100，精确 **0.01mm** 网格（占 ~91%）
  - >100mm 的大件 → 自适应缩小（s<100）刚好塞进盒子，**铺满 10000 格**（相对精度 1/10000）
- **平移进正卦限**：坐标全部 ≥1、≤10000（用缩放后真实包围盒定平移量）
- **每模型存 `scale`**：下游 ÷scale 恢复绝对尺寸
- **2 次执行验证**：缩放后几何 = 原始×scale（忠实）且严格落盒，不合格的剔除

---

## 2. 最终用到的脚本（按依赖）

```
convert_1m.py          ← 主驱动: 流式只读HF代码列, 常驻worker池, 每源文件出parquet, 可断点续传
  └─ convert_fast.py   ← 每模型逻辑: 执行原始拿bbox→定scale→AST缩放→执行缩放后验证→平移
       ├─ bbox_persistent.py  ← 常驻worker: import cadquery一次, 执行代码返回包围盒
       └─ koor_transform.py   ← ⭐核心: AST把长度参数×scale取整(语义类型传播), 防退化min-clamp

recover_1m.py          ← 恢复pass: 长超时(90s)+min-clamp 救回失败的模型, 复用convert_fast
verify_fast.py         ← 并行校验几何落[1,10000] (用bbox_persistent)
peek_1m.py             ← 随时查看进度+抽样
viz_koor.py            ← 渲染 原始vs转换后 对比图
```

**其余 .py 是开发过程产物**（survey*/scan_global_max/find_global_scale/convert_dataset/
convert_full/convert_worker/recover_timeouts/validate*/verify_box/inspect_fail/worker_persistent），
**已弃用，可忽略或删除**。

---

## 3. 运行命令（singularity 环境）

```bash
cd /home/qinyuan_fan/cadllm/workspace

# 全量转换 1M 的某个 split (train/val/test), 可断点续传(已存在的源文件跳过)
singularity exec instance://cadllm python Zero-To-CAD-Baseline/scripts/koor/convert_1m.py \
    --split train --timeout 20 --workers 16 --outdir Zero-To-CAD-Baseline/data/koor_1m

# 恢复失败的(长超时90s, 救回率~22%), 写 <源文件>.rec.parquet, 可续传
singularity exec instance://cadllm python Zero-To-CAD-Baseline/scripts/koor/recover_1m.py \
    --timeout 90 --workers 16 --dir Zero-To-CAD-Baseline/data/koor_1m/train

# 查看进度+抽样
singularity exec instance://cadllm python Zero-To-CAD-Baseline/scripts/koor/peek_1m.py

# 校验落盒
singularity exec instance://cadllm python Zero-To-CAD-Baseline/scripts/koor/verify_fast.py \
    <某个.parquet> 60 12
```

后台跑用 `nohup ... > log 2>err &`。进程是常驻worker池, 卡死的自动90s强杀重启。

---

## 4. 输出数据位置

```
Zero-To-CAD-Baseline/data/koor_1m/
├── train/<原文件名>.parquet        主转换 (819,846 行)
├── train/<原文件名>.rec.parquet    恢复救回 (持续增长, glob *.parquet 自动并入)
├── train/<原文件名>.dropped.jsonl  被丢的模型(uuid/code/stage/error)
├── val/*.parquet
└── test/*.parquet
```
（另有 100k 子集旧产物 `koor_box10k/{train,test}.parquet`）

**读取**（自动含主转换+救回）：
```python
import glob, pyarrow.parquet as pq, pyarrow as pa
files = glob.glob('Zero-To-CAD-Baseline/data/koor_1m/train/*.parquet')
t = pa.concat_tables([pq.read_table(f) for f in files])
```

### 列 schema
| 列 | 含义 |
|---|---|
| `uuid` | 原数据集 id |
| `cadquery_file` | **转换后**代码 (参数×scale, 末尾追加 translate 进 [1,10000]) |
| `cadquery_file_orig` | **原始**未改动代码 |
| `scale` | 该模型的缩放系数 (≤100mm为100, 大件<100) |
| `max_dim_mm` | 原始最长边(mm) |
| `offs` | 平移量 [ox,oy,oz] (整数, JSON字符串) |
| `n_scaled` | 缩放了几个长度字面量 |

---

## 5. 下游用法 ⚠️ 重要

**生成 [1,10000] 点云时, 不要执行缩放后代码**（坐标放大让 OCCT 慢 300-500倍）。
几何变换可交换, 直接变换原始点云即可：
```
[1,10000]点云 = 原始模型点云 × scale + offs
```
即: 从 `cadquery_file_orig` 采样点云(快, 0.2s) → 点坐标 ×scale +offs → 得到落盒点云。
结果与执行 `cadquery_file` 采样完全一致, 但快几百倍。

**训练**: `cadquery_file` 作为代码token目标; 坐标÷10000→[0,1]喂网络; 后处理预测值÷scale还原绝对mm。

---

## 6. 质量与统计

- 落盒率 **100%**(抽样验证 train/val/test)
- 救回的 = 同标准(2次执行验证), 12个抽样 忠实12/12 落盒11/12(1个大件贴0边界仍有效)
- 保留率 ~84% + 恢复救回; 丢的: timeout(54%, 大坐标慢)、scaled执行失败(BRep/退化)、
  unfaithful(9%, 如cskHole名字-位置冲突)、orig本身崩(1.3%, 数据集自带瑕疵无救)
- 大件(>100mm, ~8%)精度变粗但相对精度满10000格, 后处理还原绝对尺寸 → 不影响形状学习

## 7. 已知坑(改 koor_transform 时注意)
- `_radius` 别误判成 `radians`(角度); `factor/ratio` 要判成比例(无量纲)
- 乘除下的字面量不缩放(`width*0.5`/`(i+1)*spacing` 里的 0.5/1)
- cskHole/cboreHole 的参数名(angle)与位置(diameter)可能冲突 → 这类会被忠实校验剔除
