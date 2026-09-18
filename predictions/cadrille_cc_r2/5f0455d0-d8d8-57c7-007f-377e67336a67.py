import cadquery as cq
result = cq.Workplane('XY').box(20,20,5)
result = result.edges().fillet(2)
