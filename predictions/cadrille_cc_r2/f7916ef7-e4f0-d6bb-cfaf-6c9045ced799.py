import cadquery as cq
result = cq.Workplane('XY').box(10,10,10).faces('>Z').workplane().cskHole(5,2,5)
