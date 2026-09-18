"""
只下载 cad-recode 的 val/ 文件夹（一堆 .py，整体仅 ~352KB）。
小文件不易触发大文件 HEAD 校验问题。主站限流时可多试或换网络。

用法:
    python dl_cadrecode_val.py
下载到: scripts/data_cache/cadrecode_val/
"""
import os
os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", "60")
from huggingface_hub import snapshot_download

OUT = os.path.join(os.path.dirname(__file__), "data_cache", "cadrecode_val")
os.makedirs(OUT, exist_ok=True)
print("[*] 下载 filapro/cad-recode  val/ ...", flush=True)
p = snapshot_download(
    repo_id="filapro/cad-recode", repo_type="dataset",
    allow_patterns=["val/*"], local_dir=OUT,
)
print("[+] 下载完成:", p, flush=True)
n = sum(len(fs) for _, _, fs in os.walk(OUT))
print("[+] 文件数:", n, flush=True)
