import cadquery as cq
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
outer_radius = outer_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 6
hole_radius = outer_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.edges().chamfer(chamfer_size)
result = solid
