import cadquery as cq

channel_length = 80.0
channel_height = 20.0
web_thickness = 4.0
flange_thickness = 6.0
flange_extension = 12.0
flange_height = flange_thickness

total_width = web_thickness + flange_extension

groove_width = 8.0
groove_depth = 2.0

hole_diameter = 3.0
countersink_diameter = 5.5
countersink_angle = 82.0
hole_spacing = 10.0
chamfer_size = 0.5

base = cq.Workplane("XY").box(total_width, channel_height, channel_length)
cut_void = cq.Workplane("XY").center(total_width/2 - web_thickness/2, 0).box(web_thickness, channel_height - 2*flange_thickness, channel_length + 2)
result = base.cut(cut_void)

groove = cq.Workplane("XY").center(-total_width/2 + web_thickness - groove_depth/2, 0).box(groove_depth, groove_width, channel_length + 2)
result = result.cut(groove)

holes_along = int(channel_length / hole_spacing) + 1
result = result.faces("<X").workplane(invert=True).rarray(hole_spacing, 0, holes_along, 1).cskHole(hole_diameter, countersink_diameter, countersink_angle, web_thickness)

result = result.edges("|Z").chamfer(chamfer_size)
