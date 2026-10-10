# -*- coding: utf-8 -*-
"""Leak-free assembly split, derived from the released part split (splits/*.txt).

Rule: an assembly takes the split shared by ALL of its bodies. A two-part assembly whose
bodies fall into different part splits is quarantined, because assigning it to either
side would place a body of one split inside an assembly of the other. An assembly built
on a body outside the curated 10000-part set, or on a non-executing body, gets no split.

(Replaces the earlier documented rule "two-part assemblies whose parts fall in different
splits go to test", which would have put training bodies inside 31 test assemblies.)
Writes splits/assemblies.json and updates the rule text in splits/splits.json.
"""
import os as _os
_ROOT = _os.environ.get('COMPLEXCAD_ROOT') or _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))  # repository root
import os, json, collections

ROOT = _ROOT
S = os.path.join(ROOT, 'splits')
split_of = {}
for f, tag in (('test_400.txt', 'test'), ('val_100.txt', 'val'), ('train.txt', 'train'),
               ('quarantine_near_duplicates.txt', 'quarantine'), ('non_executing_18.txt', 'nonexec')):
    for l in open(os.path.join(S, f), encoding='utf-8'):
        u = l.strip()
        if u and u[:12] not in split_of:          # the one test/non-exec double entry keeps 'test'
            split_of[u[:12]] = tag
out = {}
for folder, kind in (('assemblies_slim', 'single'), ('two_part_assemblies_slim', 'two')):
    for n in sorted(os.listdir(os.path.join(ROOT, '1m_Convert', folder))):
        if not n.endswith('__asm' if kind == 'single' else '__two'):
            continue
        head = n.split('__')[0]
        bodies = [head[:12]] if kind == 'single' else [p[:12] for p in head.split('_')[:2]]
        tags = [split_of.get(b, 'outside') for b in bodies]
        if 'outside' in tags or 'nonexec' in tags:
            out[n] = 'none'
        elif len(set(tags)) == 1:
            out[n] = tags[0]
        else:
            out[n] = 'quarantine'
counts = collections.Counter(out.values())
json.dump(dict(rule=__doc__.strip().split('\n\n')[1], counts=dict(counts), assignment=out),
          open(os.path.join(S, 'assemblies.json'), 'w', encoding='utf-8'), indent=1)
sj = json.load(open(os.path.join(S, 'splits.json'), encoding='utf-8'))
old = 'assemblies inherit the split of their base part(s), two-part assemblies whose parts fall in different splits go to test'
new = ('assemblies take the split shared by all their bodies (splits/assemblies.json); two-part assemblies whose '
       'bodies fall in different splits are quarantined; assemblies on a body outside the curated set or on a '
       'non-executing body get no split')
assert old in sj['rule'], 'rule text not found'
sj['rule'] = sj['rule'].replace(old, new)
json.dump(sj, open(os.path.join(S, 'splits.json'), 'w', encoding='utf-8'), indent=1)
print(dict(counts), 'total', sum(counts.values()))
