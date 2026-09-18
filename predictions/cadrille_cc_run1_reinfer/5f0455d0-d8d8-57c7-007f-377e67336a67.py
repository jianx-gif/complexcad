import cadquery as cq
result = cq.Workplane('XY').box(20,20,10).edges().chamfer(1)
