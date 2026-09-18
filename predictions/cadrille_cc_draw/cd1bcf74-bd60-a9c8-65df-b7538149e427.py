import cadquery as cq
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
base_thickness = 4.0
rib_height = 2.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 8
chamfer_distance = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, base_thickness)
    .lineTo(inner_radius, base_thickness)
    .lineTo(inner_radius, base_thickness + rib_height)
    .lineTo(inner_radius, base_thickness + rib_height)
    .lineTo(outer_radius, base_thickness + rib_height)
    .lineTo(outer_radius, base_thickness + rib_height)
    .lineTo(0, base_thickness + rib_height)
    .close()
)
result = (
    profile
    .revolve()
    .edges()
    .chamfer(chamfer_distance)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .cutBlind(-rib_height)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .cutBlind(-rib_height)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .cutBlind(-rib_height)
)
