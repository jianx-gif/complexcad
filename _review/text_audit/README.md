# 文本描述人工审查（200 条）/ Text-description audit (200 descriptions)

批注 #91。抽样：从 10000 件释出零件中按 seed 42 随机抽 200 件（2026-09-13）。
Sample: 200 of the 10000 released parts, random.seed(42), drawn 2026-09-13.

## 文件 / Files

- `checklist.csv` — 填这张表。每行一件，列见下。/ Fill this sheet, one row per part.
- `items/NNN_xxxxxxxx/` — 每件的素材：`description.txt`（被审查的描述）、`cadquery.py`（程序 = 真值）、
  `image_0.png`、`image_3.png`（两张渲染图）。/ Per-part material: the description under review, the program
  (ground truth) and two renders.
- `sample_200.md` — 同样的描述与程序并排放在一个文件里，方便连续阅读。/ The same, side by side in one file.

## 怎么判 / How to judge

对每条描述，对照程序（必要时看渲染图），四列各填 1（合格）或 0（不合格）：

| 列 | 合格（1）的条件 | 常见不合格 |
|---|---|---|
| `ops_sequence_correct` | 描述列出的建模步骤就是程序执行的操作，**而且顺序是程序的构造顺序** | 顺序不对；列了程序没做的操作；把草图元素（polyline、rect）当建模步骤 |
| `dimensions_correct` | 描述引用的**每个**数值在程序里就是那个值，**而且类别对**（半径就是半径、角度就是角度） | 值错；半径写成直径；角度归到距离类；计数当成尺寸 |
| `intent_plausible` | "Design intent" 那句对这个零件说得通 | 说是回转体但零件是板件；说薄壁但零件是实心 |
| `reads_naturally` | 一段话是通顺的工程英文 | 语法错；重复；含义不清 |

只要有一处错就填 0（宁严勿宽），并在 `notes` 用关键词写原因：
`order` / `class: 参数名` / `value: 参数名` / `intent` / `wording`。`reviewer` 填姓名缩写。

For each description, compare it with the program (and the renders where needed) and mark 1 (correct) / 0 (wrong):
ops_sequence_correct = the listed steps are the program's operations in construction order; dimensions_correct =
every quoted value is the program's value with the right meaning (radius vs diameter, angle vs distance);
intent_plausible = the design-intent sentence is a fair reading of the part; reads_naturally = readable engineering
English. Any single fault gives 0; write the reason in `notes` (order / class: name / value: name / intent / wording).

## 结果怎么用 / What is computed

每列的错误率、五类错误的分布、出错件的 UUID 清单，写入论文 §4.6（替换"人工审查待做"）。
Per-column error rate, distribution over the five fault types, UUID list of faulty descriptions; reported in Sec. 4.6.

## 结果（2026-09-17）/ Result

评审 CX，200 条；`result_text_audit.json`。ops_sequence_correct 6/200、dimensions_correct 200/200、intent_plausible 200/200、reads_naturally 200/200。不合格原因全部为"order"：步骤列表按解析器遇到调用的顺序排列并把草图元素（polyline/rect/circle）当作建模步骤列在末尾（188/194 条不合格描述含此类条目，其中 152 条以草图元素结尾，6 条合格描述不含）。写入论文 §4.5、结论、摘要。
