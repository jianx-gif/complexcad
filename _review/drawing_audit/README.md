# 工程图双人盲审（200 张）/ Two-reviewer blind audit of 200 drawings

批注 #101（及 #92/#93）。抽样：seed 42，200 张零件图，抽自补回前的 9980 件（2026-09-13 之前）。
Sample: 200 part drawings, random.seed(42), drawn from the 9980 models present before the restoration of 2026-09-13.

## 文件 / Files

- `sheets/NNN_xxxxxxxx_drawing.png` — 被审查的图纸。/ The drawing under review.
- `sheets/NNN_xxxxxxxx_render.png` — 同一零件的渲染图，用来判断视图和尺寸对不对。/ A render of the same part, for reference.
- `checklist_A.csv`（评审 A，作者的同学）、`checklist_B_zh.csv`（评审 B，作者本人，中文表头）— 两位评审各填一份（`checklist.csv` 是空白母本；`checklist_B_zh.as_filled_0916.csv` 是 B 表 9 月 16 日的中间状态）。/ One sheet per reviewer: A by a fellow student of the author, B by the author (Chinese header); `checklist.csv` is the blank template.
- 图纸和渲染图（`sheets/`）在数据记录里，不在代码仓库里。/ The images in `sheets/` are in the data record, not in the code repository.

## 规则 / Protocol

1. 两位评审**各自独立**填自己的表，填完之前**不交流、不看对方的表**。
   Two reviewers with drafting experience fill their own sheet independently; no discussion until both are done.
2. 每张图六列各填 1（合格）或 0（不合格）；有问题在 `notes` 写一句；`reviewer` 填缩写。
3. 一张图约 1 分钟，200 张约 3–4 小时，可以分几次。

| 列 | 合格（1）的条件 |
|---|---|
| `views_correct` | 三个正交视图投影关系正确（第一角法），视图布局合理 |
| `dims_correct` | 标出的尺寸数值和位置对（数值与渲染图/形状一致，箭头指向正确的特征） |
| `dims_missing` | **没有**漏掉关键尺寸（总体尺寸、孔径、孔位）；有漏标填 0 |
| `dims_duplicate_or_conflict` | **没有**同一尺寸重复标注或互相矛盾的标注；有则填 0 |
| `text_line_collision` | 尺寸文字**没有**被视图线、尺寸线压住；有则填 0 |
| `scale_titleblock_ok` | 比例合理（图不太小也不出框）、标题栏字段完整 |

views_correct = first-angle projections consistent and sensibly placed; dims_correct = stated values and
placements right; dims_missing = no key dimension missing (0 if any is); dims_duplicate_or_conflict = no
repeated or contradictory dimension (0 if any); text_line_collision = no dimension text crossed by a line
(0 if any); scale_titleblock_ok = sensible scale and complete title block.

表 B 的表头是中文，与英文列一一对应：序号=idx、图纸文件=drawing_path、视图正确=views_correct、尺寸正确=dims_correct、无漏标=dims_missing、无重复或矛盾标注=dims_duplicate_or_conflict、文字无压线=text_line_collision、比例与标题栏合格=scale_titleblock_ok、评审=reviewer、备注=notes。每列同样填 1（合格）或 0（不合格）。
Sheet B carries Chinese column names in the same order as the English ones above.

## 结果怎么用 / What is computed

两位评审逐列的一致率与 Cohen's kappa，各列的不合格率（两人都判 0 / 至少一人判 0），写入论文 §4.7、§2.4 和结论。
Per-column agreement and Cohen's kappa between the reviewers, per-column fault rates (both / at least one);
reported in Sec. 4.7, Sec. 2.4 and the conclusion.

## 结果（2026-09-17）/ Result

表 A（评审 RA，2026-09-17 00:32）与表 B（作者，`checklist_B_zh.csv`，2026-09-16 23:19）各 200 行；`result_double_review.json`。

| 列 | A 不合格 | B 不合格 | 两人都 | 至少一人 | 一致 /200 | kappa |
|---|---|---|---|---|---|---|
| views_correct | 1 | 3 | 1 | 3 | 198 | 0.50 |
| dims_correct | 3 | 1 | 1 | 3 | 198 | 0.50 |
| dims_missing | 67 | 10 | 8 | 69 | 139 | 0.13 |
| dims_duplicate_or_conflict | 93 | 0 | 0 | 93 | 107 | 0.00 |
| text_line_collision | 96 | 19 | 18 | 97 | 121 | 0.18 |
| scale_titleblock_ok | 1 | 0 | 0 | 1 | 199 | 0.00 |

全部格子一致 962/1200（80.2 %）；至少一项不合格的图：A 167、B 31、两人都 30。写入论文 §4.7（tab:draw-human）、§2.4、第 1 章贡献、结论、摘要。

评审身份（2026-09-18 作者确认）：表 A = 机械工程专业同学，表 B = 作者本人；两人均受过技术制图训练。论文题注按此措辞。
