import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 20.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
fillet_radius = 2.0
chamfer_distance = 1.0
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2, 0)
    .lineTo(outer_diameter / 2, 0)
    .lineTo(outer_diameter / 2, thickness)
    .lineTo(inner_diameter / 2, thickness)
    .close()
)
rib = (
    profile
    .revolve(360)
    .edges()
    .fillet(fillet_radius)
)
rib = (
    rib
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
)
rib = (
    rib
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
)
rib = (
    rib
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
)
rib = (
    rib
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
)
rib = (
    rib
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
)
rib = (
    rib
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
)
rib = (
    rib
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
)
rib = (
    rib
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = rib
