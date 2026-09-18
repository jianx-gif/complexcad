import cadquery as cq
result = cq.Workplane('XY').box(10,10,2).faces('>Z').cskHole(3,5,1)
