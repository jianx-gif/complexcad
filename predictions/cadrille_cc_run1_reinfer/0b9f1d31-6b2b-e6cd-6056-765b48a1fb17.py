import cadquery as cq
result = cq.Workplane('XY').box(10,10,10).edges().chamfer(1)
