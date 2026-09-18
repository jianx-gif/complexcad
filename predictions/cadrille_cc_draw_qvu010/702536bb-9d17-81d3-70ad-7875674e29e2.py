import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
wall_thickness = 5.0
inner_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 6
outer_radius = outer_diameter / 2.0
inner_radius = inner_radius + wall_thickness
inner_radius = inner_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, inner_radius)
    .lineTo(inner_radius + wall_thickness, inner_radius)
    .lineTo(inner_radius + wall_thickness, inner_radius + wall_thickness)
    .lineTo(inner_radius + wall_thickness, inner_radius + wall_thickness)
    .lineTo(inner_radius, inner_radius + wall_thickness)
    .lineTo(inner_radius, inner_radius)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
hole_positions = [
    (inner_radius + wall_thickness + hole_spacing / 2.0, inner_radius + hole_spacing / 2.0),
    (inner_radius + wall_thickness + hole_spacing / 2.0, inner_radius + hole_spacing / 2.0),
    (inner_radius, inner_radius + hole_spacing / 2.0),
    (inner_radius, inner_radius + hole_spacing / 2.0),
    (inner_radius, inner_radius + hole_spacing / 2.0),
    (inner_radius, inner_radius + hole_spacing / 2.0),
]
solid = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(outer_radius)
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)
solid = solid.cut(hole_positions)
result = solid
