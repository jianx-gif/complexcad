"""排查 cad-recode val 里没匹配到 extrude 的那 ~11% 是什么。"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))  # repository root
_DS = _os.environ.get('CADRECODE_DATASETS') or _ROOT + '/datasets'  # CAD-Recode dataset copies, see README
import glob, re, os
from collections import Counter

VAL = _DS + '/cadrecode_val/val'
files = sorted(glob.glob(os.path.join(VAL, "*.py")))
print("总文件:", len(files))

no_extrude = []
extrude_method_variants = Counter()  # 看 extrude 是不是写成别的形式
for fp in files:
    code = open(fp, encoding="utf-8").read()
    if not re.search(r"\bextrude\b", code, re.IGNORECASE):
        no_extrude.append(fp)
    # 统计所有 .xxx( 方法调用，看没extrude的用了什么
print("没匹配到 extrude 的文件数:", len(no_extrude), f"({100*len(no_extrude)/len(files):.1f}%)")
print()

# 看没 extrude 的样本里到底用了哪些 CadQuery 方法
method_counter = Counter()
print("===== 没 extrude 的样本代码（前8个完整打印）=====")
for fp in no_extrude[:8]:
    code = open(fp, encoding="utf-8").read()
    print(f"\n--- {os.path.basename(fp)} ---")
    print(code.strip())
    for m in re.findall(r"\.([a-zA-Z_]+)\(", code):
        method_counter[m] += 1

print("\n===== 没 extrude 样本里出现的所有方法（频次）=====")
for m, c in method_counter.most_common(30):
    print(f"  {m}: {c}")
