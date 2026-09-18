"""数据源配置(测试集/训练集切换 + HPC 分片), 全部批处理脚本共用。

默认读 ROOT/test/*.parquet(本机测试集, 与历史行为一致)。两个环境变量:

  Z2C_PARQUET_GLOB   parquet 文件 glob。指向训练集时如:
                     /data/zero-to-cad/train/*.parquet
  Z2C_SHARD          "i/N"(i 从 0 起)。把排序后的文件列表按 files[i::N] 交错
                     切片 -> N 个 HPC 阵列任务各处理一片, 互不重叠。
                     交错切片使各片文件大小均匀。

环境变量会自动传给 subprocess 启动的 worker(produce_one/produce_two_one/
scan_two_chunk), 因此只需在作业脚本里 export 一次。
"""
import os, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_GLOB = os.path.join(ROOT, "test", "*.parquet")


def parquet_files():
    """返回本任务应处理的 parquet 文件列表(已按 Z2C_SHARD 切片)。"""
    pat = os.environ.get("Z2C_PARQUET_GLOB") or DEFAULT_GLOB
    files = sorted(glob.glob(pat))
    shard = os.environ.get("Z2C_SHARD")
    if shard:
        i, n = (int(x) for x in shard.strip().split("/"))
        if not (0 <= i < n):
            raise ValueError(f"Z2C_SHARD={shard}: 需要 0<=i<N")
        files = files[i::n]
    return files
