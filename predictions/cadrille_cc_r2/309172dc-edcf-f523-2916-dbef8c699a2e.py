import cadquery as cq
outer_radius = 30.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
chamfer_distance = 1.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 6
hole_radius = hole_diameter / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(outer_radius, wall_thickness)
    .lineTo(outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().center(0, 0).circle(hole_radius).cutBlind(-hole_count)
solid = solid.faces(">Z").workplane().center(hole_radius, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(hole_radius, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(hole_radius, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(hole_radius, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(hole_radius, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(hole_radius, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(hole_radius, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(hole_radius, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(hole_radius, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(hole_radius, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(hole_radius, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(hole_radius, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(hole_radius, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(hole_radius, 0).hole(hole_diameter)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
