import cadquery as cq
outer_radius = 45.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
chamfer_distance = 1.0
hole_diameter = 5.0
hole_spacing = 15.0
hole_count = 6
hole_count = 3
hole_count = 3
chamfer_distance = 0.5
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(chamfer_distance)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(chamfer_distance)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(chamfer_distance)
result = outer_cyl.cut(inner_cyl)
result = result.edges().fillet(inner_radius)
result = result.faces('>Z').edges().chamfer(chamfer_distance)
