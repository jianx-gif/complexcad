import cadquery as cq
result = cq.Workplane('XY').box(20,20,5).faces('>Z').workplane().cskHole(5,2,5)
