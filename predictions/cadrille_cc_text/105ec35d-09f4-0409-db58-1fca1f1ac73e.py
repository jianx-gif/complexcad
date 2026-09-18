import cadquery as cq
result = cq.Workplane('XY').box(10,80,8).translate((0,0,8))
result = result.union(2)
