import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 10.0
inner_radius = inner_radius - wall_thickness
chamfer_distance = 1.0
rib_width = 5.0
rib_height = 10.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 6
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(inner_radius)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius).translate((0,0,0))
result = outer_cyl.cut(inner_cyl)
result = result.edges().fillet(inner_radius)
result = result.faces('>Z').workplane().hole(inner_radius * 2)
result = result.faces('>Z').workplane().hole(inner_radius * 2)
