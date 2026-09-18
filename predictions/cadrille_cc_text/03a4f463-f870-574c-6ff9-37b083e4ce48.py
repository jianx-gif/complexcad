import cadquery as cq
result = cq.Workplane('XY').box(80,40,5).faces('>Z').workplane().hole(5)
