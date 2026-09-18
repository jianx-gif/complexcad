import cadquery as cq
knob_outer_radius = 20.0
knob_shoulder_radius = 12.0
knob_base_height = 12.0
knob_shoulder_height = 8.0
shaft_radius = 4.0
shaft_radius = 14.0
fillet_radius = 2.0
chamfer_size = 1.0
mount_hole_radius = 2.0
mount_hole_circle_radius = 14.0
mount_hole_count = 4
mount_hole_radius = mount_hole_radius + 2.0
knob_body = (
    cq.Workplane("XY")
    .circle(knob_outer_radius)
    .extrude(knob_base_height)
)
knob_body = (
    cq.Workplane("XY")
    .circle(knob_outer_radius)
    .extrude(knob_base_height)
    .translate((0, 0, knob_base_height))
)
knob_body = knob_body.union(knob_body)
knob_body = (
    knob_body
    .faces(">Z")
    .workplane()
    .hole(shaft_radius * 2)
)
knob_body = (
    knob_body
    .faces(">Z")
    .workplane()
    .hole(shaft_radius * 2)
)
knob_body = (
    knob_body
    .faces(">Z")
    .workplane()
    .polarArray(mount_hole_circle_radius, 0, 360, mount_hole_count)
    .hole(mount_hole_radius * 2)
)
knob_body = knob_body.union(knob_body)
knob_body = knob_body.edges().fillet(fillet_radius)
result = knob_body
