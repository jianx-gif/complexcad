import cadquery as cq
outer_radius = 45.0
inner_radius = 20.0
inner_radius = 30.0
wall_thickness = 2.0
chamfer_distance = 0.5
hole_diameter = 5.0
hole_depth = 10.0
hole_spacing = 12.0
hole_count = 8
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, inner_radius)
    .lineTo(inner_radius + wall_thickness, inner_radius)
    .lineTo(inner_radius + wall_thickness, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges("|Z").chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.edges("|Z").chamfer(chamfer_distance)
result = solid
