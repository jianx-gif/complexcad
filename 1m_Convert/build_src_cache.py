"""建 uuid->源码 缓存, 供 produce_two_one 查表加速(免每配一对都重扫 parquet)。

- build_cache(uuids): 对给定 uuid 集合, 扫 parquet 一遍, 每个写 _srccache/<uuid>.py
  (只写缺失的, 幂等)。batch_two 建完候选池后直接调它(传池中 uuid), 使 HPC 上生成
  自动获得加速, 无需手动步骤。
- 独立运行(python build_src_cache.py): 从 two_pool.json 读 uuid 后调 build_cache。

produce_two_one 缺缓存时会自动回退扫 parquet, 故本步骤失败不影响正确性, 只影响速度。
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import pyarrow.parquet as pq
import dataset_source

SCRATCH = os.environ.get("CLAUDE_SCRATCH", HERE)
POOL = os.path.join(SCRATCH, "two_pool.json")
CACHE = os.path.join(HERE, "_srccache")


def build_cache(uuids):
    """给定 uuid 可迭代对象, 把其源码扫出并写入 _srccache/<uuid>.py(只写缺失)。
    返回 (新写数, 未找到数)。"""
    os.makedirs(CACHE, exist_ok=True)
    want = set(uuids)
    have = set(os.path.splitext(f)[0] for f in os.listdir(CACHE))
    todo = want - have
    if not todo:
        print("[cache] 已齐 %d, 跳过。" % len(want), flush=True)
        return 0, 0
    print("[cache] 目标 %d, 待建 %d ..." % (len(want), len(todo)), flush=True)
    n = 0
    for f in dataset_source.parquet_files():
        if not todo:
            break
        pf = pq.ParquetFile(f)
        for rg in range(pf.num_row_groups):
            for row in pf.read_row_group(
                    rg, columns=["uuid", "cadquery_file"]).to_pylist():
                u = row["uuid"]
                if u in todo:
                    code = row["cadquery_file"]
                    if isinstance(code, (bytes, bytearray)):
                        code = bytes(code).decode("utf-8", "replace")
                    open(os.path.join(CACHE, u + ".py"), "w",
                         encoding="utf-8").write(code)
                    todo.discard(u)
                    n += 1
            if not todo:
                break
    print("[cache] 完成: 新写 %d, 未找到 %d  -> %s" % (n, len(todo), CACHE),
          flush=True)
    return n, len(todo)


def main():
    want = []
    if os.path.isfile(POOL):
        want = [e["uuid"] for e in json.load(open(POOL, encoding="utf-8"))]
    print("目标 uuid(候选池): %d" % len(want), flush=True)
    build_cache(want)


if __name__ == "__main__":
    main()
