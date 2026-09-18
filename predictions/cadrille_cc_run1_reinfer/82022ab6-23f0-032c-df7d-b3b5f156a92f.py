import cadquery as cq
outer_radius = 10.0
inner_radius = 10.0
inner_radius = 10.0
inner_radius = inner_radius - inner_radius
chamfer_size = 2.0
hole_diameter = 6.0
hole_spacing = 12.0
hole_count = 12
chamfer_distance = 0.5
outer = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
inner = inner_radius - inner_radius
result = outer.cut(inner)
result = result.edges().fillet(inner_radius)
result = result.faces('>Z').workplane().hole(inner_radius)
result = result.faces('>Z').workplane().circle(inner_radius).extrude(outer_radius)
