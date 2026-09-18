import cadquery as cq
outer_radius = 20.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 3
hole_offset = 10.0
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .lineTo(inner_radius, wall_thickness + inner_radius)
    .close()
)
solid = profile.extrude(chamfer_size)
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).circle(hole_diameter/2).cutBlind(-hole_offset)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
solid = solid.edges("|Z").chamfer(chamfer_size)
result = solid
