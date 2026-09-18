import cadquery as cq
result = cq.Workplane('XY').polarArray(6, 0, 360, 10).circle(2).extrude(2)
