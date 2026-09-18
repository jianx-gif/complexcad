"""把转换后(量化整数坐标)的 CadQuery 脚本按 uuid 提取成独立 py 文件,
方便直接读取。来源 = 主转换 + 恢复 pass 两个 parquet 的 cadquery_file 列。

输出: 1m_Convert/converted_py/<uuid>/cadquery.py   (转换后量化代码)
      并在每个文件夹附 koor.json (scale/offs/max_dim_mm) 便于还原。
用法: python extract_converted_py.py [N]   (默认全部; N=只取前 N 个)
"""
import sys, os, json
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)          # 1m_Convert/ (脚本移入 koor/ 后, 数据目录在上一级)
OUT = os.path.join(PARENT, "converted_py")
SRC = [os.path.join(PARENT, "_testrun", "out", "test.parquet"),
       os.path.join(PARENT, "_testrun", "rec", "test.rec.parquet")]


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    os.makedirs(OUT, exist_ok=True)
    written = 0
    for path in SRC:
        if not os.path.exists(path):
            print(f"[skip] 不存在: {path}", flush=True)
            continue
        t = pq.read_table(path, columns=["uuid", "cadquery_file", "scale",
                                         "offs", "max_dim_mm"])
        rows = t.to_pylist()
        for r in rows:
            if n and written >= n:
                break
            u = r["uuid"]
            code = r["cadquery_file"]
            if isinstance(code, (bytes, bytearray)):
                code = bytes(code).decode("utf-8", "replace")
            d = os.path.join(OUT, u)
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "cadquery.py"), "w", encoding="utf-8").write(code)
            json.dump({"scale": r["scale"], "offs": r["offs"],
                       "max_dim_mm": r["max_dim_mm"]},
                      open(os.path.join(d, "koor.json"), "w", encoding="utf-8"),
                      ensure_ascii=False, indent=2)
            written += 1
        print(f"  {os.path.basename(path)}: 累计写出 {written}", flush=True)
        if n and written >= n:
            break
    print(f"完成: {written} 个转换后脚本 -> {OUT}\\<uuid>\\cadquery.py", flush=True)


if __name__ == "__main__":
    main()
