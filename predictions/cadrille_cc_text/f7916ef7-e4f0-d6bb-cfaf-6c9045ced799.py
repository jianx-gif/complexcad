import cadquery as cq
result = cq.Workplane('XY').box(10,10,5).cskHole(2,4,45)
