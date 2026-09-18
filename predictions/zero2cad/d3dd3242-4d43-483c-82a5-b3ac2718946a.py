import cadquery as cq
result = cq.Workplane('XY').box(80,60,40).faces('>Z').edges().fillet(1.5)
