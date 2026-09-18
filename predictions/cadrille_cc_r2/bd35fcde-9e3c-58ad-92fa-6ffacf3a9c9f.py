import cadquery as cq
result = cq.Workplane('XY').box(10,10,10).faces('>Z').workplane().cskHole(1,2,5)
