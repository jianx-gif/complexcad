import cadquery as cq
result = cq.Workplane('XY').circle(40).extrude(60).shell(2)