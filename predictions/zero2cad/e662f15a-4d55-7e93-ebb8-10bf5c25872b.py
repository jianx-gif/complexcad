import cadquery as cq
result = cq.Workplane('XY').rect(80,40).extrude(15).faces('>Z').edges().fillet(2)
