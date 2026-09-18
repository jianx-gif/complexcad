import cadquery as cq
result = cq.Workplane('XY').rect(80,40).extrude(8).faces('>Z').workplane().hole(5)
