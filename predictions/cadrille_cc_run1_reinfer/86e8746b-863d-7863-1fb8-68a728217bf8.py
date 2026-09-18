import cadquery as cq
outer_length = 100.0
wall_thickness = 10.0
inner_length = outer_length - 2 * wall_thickness
inner_width = inner_width - 2 * wall_thickness
inner_height = inner_height - 2 * wall_thickness
inner = cq.Workplane('XY').rect(inner_length, inner_width).extrude(10.0)
result = result.faces('>Z').workplane().rect(inner_length, inner_width).cutBlind(-10.0)
