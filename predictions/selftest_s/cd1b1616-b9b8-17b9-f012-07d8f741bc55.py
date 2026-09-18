import cadquery as cq
result = cq.Workplane('XY').box(10,10,5).faces('+Z').sketch().rect(5,5).finalize().cutBlind(-2)
