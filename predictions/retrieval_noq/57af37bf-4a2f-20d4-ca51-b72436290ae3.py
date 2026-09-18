import cadquery as cq
result = cq.Workplane('XY').box(10,10,10).edges('|Z and >Y').chamfer(0.5)
