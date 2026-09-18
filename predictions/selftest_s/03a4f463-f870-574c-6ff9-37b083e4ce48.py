import cadquery as cq
result = cq.Workplane('XY').box(80,40,8).faces('>Z').hole(5)
