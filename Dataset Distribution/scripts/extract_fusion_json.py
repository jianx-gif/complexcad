"""只从 r1.0.1.zip 解压 reconstruction 的 .json 设计序列文件（跳过 obj/png/smt/step）。"""
import zipfile, os

ZIP = r"E:\2106\datasets\r1.0.1.zip"
OUT = r"E:\2106\datasets\fusion360_recon\json"
os.makedirs(OUT, exist_ok=True)

n = 0
with zipfile.ZipFile(ZIP) as z:
    names = [x for x in z.namelist()
             if x.endswith(".json") and "/reconstruction/" in x]
    print("[*] reconstruction json 数:", len(names), flush=True)
    for name in names:
        # 拍平到 OUT 目录
        base = os.path.basename(name)
        with z.open(name) as src, open(os.path.join(OUT, base), "wb") as dst:
            dst.write(src.read())
        n += 1
        if n % 2000 == 0:
            print("    解压", n, flush=True)
print("[+] 完成，共解压 json:", n, "→", OUT, flush=True)
