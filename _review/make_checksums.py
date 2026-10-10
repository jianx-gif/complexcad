# -*- coding: utf-8 -*-
"""SHA-256 of the files a reader needs to reproduce the reported numbers:
splits, environment specs, and every result file the thesis cites. Writes checksums.txt
(sha256sum format) at the release root."""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, glob, hashlib

ROOT = _ROOT
pats = ['splits/*.txt', 'splits/*.json', 'env/*',
        '_review/exp_*.json', '_review/brepcheck_invalid.json', '_review/grabcad_manifest.csv',
        '_review/param_ranges.json', '_review/supp_scan_stats.json', '_review/supp_selection.json',
        '_review/supp_build_stats.json',
        '1m_Convert/precision_report/*.json', '1m_Convert/precision_report/*.jsonl',
        '_review/*_lora*/final_adapter/adapter_model.safetensors', '_review/*_lora*/final_adapter/adapter_config.json']
files = []
for p in pats:
    files += sorted(glob.glob(os.path.join(ROOT, p)))
files = [f for f in files if '.bak' not in os.path.basename(f)]
lines = []
for f in files:
    h = hashlib.sha256(open(f, 'rb').read()).hexdigest()
    lines.append('%s  %s' % (h, os.path.relpath(f, ROOT).replace('\\', '/')))
lines = [l for l in lines if 'exp_c4_runtime_trace' not in l]
open(os.path.join(ROOT, 'checksums.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
print(len(lines), 'files hashed')
for l in lines:
    if l.split('  ')[1] in ('splits/test_400.txt', 'splits/train.txt', 'splits/assemblies.json',
                            'env/environment-cadfit.yml', 'env/requirements-training.txt',
                            '1m_Convert/precision_report/metrics.jsonl'):
        print(l)
