import cadquery as cq
outer_diameter = 30.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, 0)
    .close()
    .revolve()
)
result = (
    profile
    .faces(">Z")
    .workplane()
    .hole(inner_radius - wall_thickness)
    .faces(">Z")
    .workplane()
    .hole(inner_radius - wall_thickness)
    .hole(inner_radius - wall_thickness)
    .edges("|Z")
    .fillet(inner_radius)
    .faces(">Z")
    .workplane()
    .rect(inner_radius, inner_radius)
    .cutBlind(-inner_radius)
)
