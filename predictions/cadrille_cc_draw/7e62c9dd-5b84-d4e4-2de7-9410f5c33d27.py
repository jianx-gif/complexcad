import cadquery as cq
outer_diameter = 50.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 4
hole_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_diameter / 2.0, 0)
    .lineTo(outer_diameter / 2.0, wall_thickness)
    .lineTo(outer_diameter / 2.0, wall_thickness + wall_thickness)
    .lineTo(outer_diameter / 2.0, wall_thickness + wall_thickness + wall_thickness)
    .lineTo(0, wall_thickness + wall_thickness + wall_thickness)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces("<Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.edges("|Z").chamfer(chamfer_size)
result = solid
