import cadquery as cq
outer_radius = 45.0
inner_radius = 30.0
wall_thickness = 2.0
inner_radius = inner_radius - wall_thickness
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 12.0
hole_count = 6
hole_count = 3
hole_count = 2
hole_spacing = 20.0
num_holes = 3
chamfer_distance = 0.5
outer_profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, outer_profile)
    .lineTo(outer_radius, outer_profile)
    .lineTo(outer_radius, outer_profile)
    .lineTo(outer_radius, 0)
    .close()
)
solid = outer_profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
