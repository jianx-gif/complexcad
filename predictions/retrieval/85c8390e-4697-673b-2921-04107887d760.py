import cadquery as cq
result = cq.Workplane('XY').polygon(12, 40).extrude(12)