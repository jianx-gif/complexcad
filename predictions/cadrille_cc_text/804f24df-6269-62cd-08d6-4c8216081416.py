import cadquery as cq
result = cq.Workplane('XY').rect(20,20).extrude(20).faces('>Z').edges().chamfer(2)
