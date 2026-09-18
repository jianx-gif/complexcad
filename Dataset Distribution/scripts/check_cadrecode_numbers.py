"""检查 cad-recode val 里的数值：是否都是整数？有无负数？有无小数？范围多大？"""
import glob, re, os
from collections import Counter

VAL = r"E:\2106\datasets\cadrecode_val\val"
files = sorted(glob.glob(os.path.join(VAL, "*.py")))
print("总文件:", len(files))

# 匹配所有数字（含负号、小数）
num_re = re.compile(r"-?\d+\.?\d*")

total = 0
n_int = 0          # 整数
n_float = 0        # 含小数点且非 .0
n_negative = 0     # 负数
all_vals = []
float_examples = []
neg_examples = []
val_min = float("inf"); val_max = float("-inf")

for fp in files:
    code = open(fp, encoding="utf-8").read()
    # 去掉 import 行避免误匹配版本号等
    for tok in num_re.findall(code):
        # 跳过空/孤立负号
        if tok in ("", "-", "."):
            continue
        try:
            v = float(tok)
        except ValueError:
            continue
        total += 1
        all_vals.append(v)
        val_min = min(val_min, v); val_max = max(val_max, v)
        if v < 0:
            n_negative += 1
            if len(neg_examples) < 10:
                neg_examples.append((os.path.basename(fp), tok))
        # 是否整数：小数部分为0
        if v == int(v):
            n_int += 1
        else:
            n_float += 1
            if len(float_examples) < 15:
                float_examples.append((os.path.basename(fp), tok))

print(f"\n总数值个数: {total}")
print(f"整数(含负整数): {n_int}  ({100*n_int/total:.2f}%)")
print(f"非整数(带小数): {n_float}  ({100*n_float/total:.2f}%)")
print(f"负数: {n_negative}  ({100*n_negative/total:.2f}%)")
print(f"数值范围: [{val_min}, {val_max}]")

print("\n--- 小数样例(文件, 值) ---")
for f, t in float_examples:
    print(f"  {f}: {t}")
if not float_examples:
    print("  （无小数，全部是整数）")

print("\n--- 负数样例 ---")
for f, t in neg_examples:
    print(f"  {f}: {t}")

# 整数是否落在某个量化网格(如0-100 / 0-255)
ints = [int(v) for v in all_vals if v == int(v)]
print("\n--- 整数分布 ---")
print(f"  整数最小: {min(ints)}  最大: {max(ints)}")
absmax = max(abs(v) for v in ints)
print(f"  绝对值最大: {absmax}")
# 看是否像 0-100 网格
in_100 = sum(1 for v in ints if -100 <= v <= 100)
print(f"  落在 [-100,100] 内的整数占比: {100*in_100/len(ints):.1f}%")
