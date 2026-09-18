import cadquery as cq
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_count = 4
hole_count = 2
hole_spacing = 15.0
num_holes = 3
chamfer_distance = 0.5
outer_profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, outer_radius - wall_thickness)
    .lineTo(outer_radius - wall_thickness, outer_radius - wall_thickness)
    .lineTo(inner_radius, outer_radius - wall_thickness)
    .close()
)
solid = outer_profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
result = solid
