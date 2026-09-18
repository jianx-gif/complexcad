import cadquery as cq
result = cq.Workplane('XY').box(10,10,2).faces('>Z').workplane().cskHole(4,2,90)
