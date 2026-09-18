import cadquery as cq

outer_radius = 80.0
outer_radius = 30.0
wall_thickness = 2.0
wall_thickness = 12.0
wall_thickness = 2.0
chamfer_distance = 1.0
chamfer_distance = 1.0
hole_diameter = 2.0
hole_count = 10
hole_count = 20
hole_count = 20
hole_count = 12
hole_count = 20
hole_spacing = 20

base = cq.Workplane('XY').box(outer_length, outer_width, outer_height, centered=(outer_length, outer_length, center=True))
result = cq.Workplane('XY').box(outer_length, outer_width, outer_height, centered=(outer_length, outer_height, center=True))
result = cq.Workplane('XY').box(outer_length, outer_height, outer_height, centered=True).translate((outer_radius, outer_height, outer_height/2 + 0.85, outer_height/2 + 0.85).translate((0, 0, outer_height/2 + 0, 0, outer_height/2 + 0)
    result = result.faces('>Z').workplane().rect(outer_width, outer_height).extrude(outer_height)
result = result.faces('>Z').workplane().rect(outer_width, outer_height).extrude(outer_height)
