# Parser audit sample

40 programs (30 Zero-To-CAD test, 10 CAD-Recode v1.5 train). For each file, mark in audit_sheet.csv (human_* columns) whether the program really calls loft/revolve/sweep/chamfer/fillet (1 = yes, 0 = no). The regex_* and ast_* columns are the two automatic parsers; disagreements between them are listed first. Human precision = agreement of human with the regex columns.
