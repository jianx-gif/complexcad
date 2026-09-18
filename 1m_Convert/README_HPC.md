# HPC 交接指南 — Zero-To-CAD 训练集(980k)装配多模态生成

本工具把 Zero-To-CAD 的 parquet 数据(与测试集同格式)批量转成**两类装配 + 全套
多模态**(STEP/STL/工程图 png+svg+dxf/BOM json/可重放装配脚本/精简 slim 版)。
已在 10k 测试集上完整验证(单件 1005 + 双件 1170, 全部通过几何校验)。
纯命令行 Python, 无 GUI、无 AI 工具依赖, 可直接在 HPC 上运行。

## 0. 拿到包先做什么

1. 把 zip 解压到**大容量工作盘**(scratch/work): 产出会写进包内的
   `1m_Convert/assemblies*/`、`two_part_assemblies*/`, 每装配 ~2-3MB。
2. 全程只需 CPU, **不需要 GPU**; 计算节点无需外网(数据与 conda 环境都在
   登录节点准备好)。
3. 之后按下面 1→5 节顺序操作即可。

## 1. 环境(一次性)

```bash
conda env create -f ../environment.yml      # 在包根目录
conda activate z2cad
# 自检(三个库版本必须匹配, cq_warehouse 已在 yml 里锁定 commit):
python -c "import cadquery, OCP; from cq_warehouse.fastener import SocketHeadCapScrew; print('OK', cadquery.__version__)"
```

## 2. 数据(登录节点下载一次)

```bash
pip install -U "huggingface_hub[cli]"
huggingface-cli download ADSKAILab/Zero-To-CAD-1m \
    --repo-type dataset --include "data/train/*" \
    --local-dir /path/to/zero2cad          # 训练集 parquet ~2200 个文件, ~300GB
```

## 3. 两个环境变量(核心开关)

| 变量 | 含义 | 例 |
|---|---|---|
| `Z2C_PARQUET_GLOB` | parquet 数据 glob(不设=本机 test/) | `/path/to/zero2cad/data/train/*.parquet` |
| `Z2C_SHARD` | `i/N` 分片(0 起), 各阵列任务互不重叠 | `$SLURM_ARRAY_TASK_ID/22` |

环境变量自动传给 worker 子进程, 只需 export 一次。

## 4. 运行(每个分片内)

```bash
export Z2C_PARQUET_GLOB="/path/to/zero2cad/data/train/*.parquet"
export Z2C_SHARD="0/22"            # 本任务的分片

# ① 单件装配(零件+ISO紧固件): 目录即 slim 数据(相对路径脚本+part+全模态)
python -X utf8 batch_assemble.py 2000 --jobs 16
# ② 双件装配(两零件螺栓夹紧): 同为 slim 数据
python -X utf8 batch_two.py 2000 --jobs 16 --scan 20000
```

- **自动源码缓存(加速)**: `batch_two.py` 建完候选池后会自动建 `_srccache/`
  (uuid→零件源码), 让并发 worker 查表取源码, 免每配一对都重扫 parquet(多 worker
  并发扫同一批 parquet 的 I/O 争抢是生成慢的主因)。此步失败不影响正确性——worker
  缺缓存会自动回退扫 parquet。`_srccache/` 是可弃中间物, 跑完可删。
- **断点续跑**: 所有步骤幂等——重跑自动跳过已完成目录("已存在 X, 待做 Y"),
  节点被抢占/超时后原命令重提交即可。
- 产出在 `assemblies/`(单件)、`two_part_assemblies/`(双件), 每目录即一条
  自包含 slim 装配数据(相对本目录; 建议整个包放在大容量工作盘上)。

## 5. SLURM 阵列模板

见 `run_train_hpc.sbatch`(22 路阵列, 每任务一个分片)。按集群实际情况改
分区名/核数/时限后 `sbatch run_train_hpc.sbatch`。

## 6. 规模与预算(基于测试集实测)

| 项 | 实测值 |
|---|---|
| 装配产出速率 | ~0.2-0.4 件/秒 (单节点 8-16 workers) |
| 每装配磁盘占用 | ~2-3 MB (含全部模态) |
| 例: 每类 5 万装配 | 产出 ~10 万目录, ~300 GB, 22 节点各 ~10-20 h |

装配目标数 N 按需设定(命令行第一个参数, 每分片各自计数)——两零件独立配对,
不必也不可能覆盖全部 980k 零件; 建议按训练需求定总量后除以分片数。

## 7. 产出结构(每个装配目录)

```
<name>/
├── assembly_cadquery.py   可重放装配脚本(slim 相对路径版)
├── assembly.json          BOM(ISO 规格) + 装配信息
├── model.step / model.stl 3D(紧固件带真 ISO 螺纹)
├── drawing.png/svg/dxf    ISO 工程图(三视图+ISO立体图+件号气泡+BOM表)
└── partA/ partB/ (或 part/)  零件源码 + 零件图
装配脚本为**相对路径 slim 版**(CQ-editor 可直接打开): 从本目录 partA/partB
(或 part/)相对加载零件, 共享 fasteners.py/library_parts.py 在输出根目录。
整个输出目录自包含、可整体拷贝。
```

归档建议: 产出为大量小文件(每装配一个目录), Lustre 类文件系统对 inode 敏感 ——
输出保持在 scratch/work 盘, 跑完按分片 `tar czf shard_i.tgz ...` 归档后再迁移。

出错反馈: 把 `logs/asm_*.out` 里的 FAIL 行与末尾统计发回给学生即可定位;
几何校验不过的装配不落盘, 失败只影响单件, 不影响整批。

问题排查: 单件某零件失败只影响该件(独立子进程+超时保护), 日志里 FAIL 行
带原因; 几何校验不过的装配不落盘, 不会产生半成品。

## 8. 唯一性与去重(设计说明)

- 上游数据集自身高度唯一: 在 10k 测试集上实测, 规范化(去注释/空白)后代码
  唯一率 99.98%(仅 2 对重复)。因此**不做**代码/几何级去重, 依赖上游唯一性;
  外推到 980k 约 0.02% 重复, 对装配产出为噪声级。
- 管线内置的防重复: 候选池 uuid 去重、配对去重(无序对+规格作 key, 排除自配)、
  输出目录幂等跳过、分片按文件切分天然不重叠。
- 双件目录名用 uuid 前 12 位(980k 规模下 8 位存在生日碰撞, 12 位期望碰撞≈0);
  解析端同时兼容历史 8 位命名。
