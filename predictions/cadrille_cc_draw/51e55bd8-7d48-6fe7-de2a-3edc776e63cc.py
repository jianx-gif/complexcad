import cadquery as cq
outer_radius = 30.0
inner_radius = 15.0
height = 20.0
wall_thickness = 2.0
chamfer_distance = 0.5
hole_diameter = 5.0
hole_depth = 10.0
hole_count = 6
hole_circle_radius = outer_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height - wall_thickness)
    .lineTo(inner_radius + wall_thickness, height - wall_thickness)
    .lineTo(inner_radius + wall_thickness, height)
    .lineTo(inner_radius + wall_thickness, height)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.edges().chamfer(chamfer_distance)
result = solid
