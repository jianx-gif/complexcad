import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 5.0
rib_height = 12.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
chamfer_size = 0.5
slot_width = 10.0
slot_length = 20.0
slot_depth = thickness / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2.0, 0)
    .lineTo(inner_diameter / 2.0, thickness / 2.0 - rib_width)
    .lineTo(inner_diameter / 2.0, thickness / 2.0 - rib_width)
    .lineTo(inner_diameter / 2.0, thickness / 2.0 - rib_width)
    .lineTo(inner_diameter / 2.0, thickness / 2.0 - rib_width)
    .lineTo(inner_diameter / 2.0, thickness / 2.0)
    .lineTo(inner_diameter / 2.0, 0)
    .close()
)
result = profile.revolve()
result = result.edges("|Z").chamfer(chamfer_size)
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=inner_diameter / 2.0 - rib_width / 2.0, startAngle=0, angle=360)
    .rect(rib_width, rib_width)
    .extrude(rib_height)
)
result = result.union(rib_count)
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=inner_diameter / 2.0, startAngle=0, angle=360)
    .rect(slot_width, slot_length)
    .cutBlind(-thickness)
)
