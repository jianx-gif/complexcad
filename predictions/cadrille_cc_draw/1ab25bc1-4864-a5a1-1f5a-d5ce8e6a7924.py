import cadquery as cq
outer_diameter = 80.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 30.0
hole_count = 4
hole_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(inner_diameter)
solid = solid.faces(">Z").workplane().hole(inner_diameter)
solid = solid.faces(">Z").workplane().hole(inner_diameter)
solid = solid.faces(">Z").workplane().hole(inner_diameter)
solid = solid.faces(">Z").workplane().hole(inner_diameter)
solid = solid.faces("<Z").workplane().hole(inner_diameter)
solid = solid.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces("<Z").edges().chamfer(chamfer_size)
result = solid
