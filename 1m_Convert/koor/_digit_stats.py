"""统计转换后量化代码里所有数值字面量的分布, 验证是否全是100的整数倍,
末位/末两位是否恒为0 (那样网络学不到个位/十位)。"""
import ast, glob, os, json
from collections import Counter
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)          # 1m_Convert/ (脚本移入 koor/ 后, 数据目录在上一级)
parqs = [os.path.join(PARENT, "_testrun", "out", "test.parquet"),
         os.path.join(PARENT, "_testrun", "rec", "test.rec.parquet")]


def nums_of(code):
    out = []
    try:
        tree = ast.parse(code)
    except Exception:
        return out
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) \
                and not isinstance(n.value, bool):
            out.append(n.value)
    return out


last1 = Counter()      # 末位 (mod 10)
last2 = Counter()      # 末两位 (mod 100)
mult100 = 0
total = 0
nonint = 0
scale_seen = Counter()
sample_nonmult = []
for pqf in parqs:
    if not os.path.exists(pqf):
        continue
    t = pq.read_table(pqf, columns=["cadquery_file", "scale"])
    codes = t.column("cadquery_file").to_pylist()
    scales = t.column("scale").to_pylist()
    for code, sc in zip(codes, scales):
        scale_seen[round(sc)] += 1
        for v in nums_of(code):
            total += 1
            if abs(v - round(v)) > 1e-9:
                nonint += 1
                continue
            iv = int(round(v))
            last1[iv % 10] += 1
            last2[iv % 100] += 1
            if iv % 100 == 0 and iv != 0:
                mult100 += 1
            elif iv != 0 and len(sample_nonmult) < 15:
                sample_nonmult.append(iv)

print(f"总数值字面量: {total}  非整数: {nonint}")
print(f"100的整数倍(非0): {mult100} ({100*mult100/max(1,total):.1f}%)")
print(f"\n末位(个位)分布 mod 10:")
for d in range(10):
    print(f"  末位={d}: {last1[d]} ({100*last1[d]/max(1,sum(last1.values())):.1f}%)")
print(f"\n非0且非100倍数的样本: {sample_nonmult}")
print(f"\nscale 分布(取整): {dict(scale_seen.most_common(8))}")
