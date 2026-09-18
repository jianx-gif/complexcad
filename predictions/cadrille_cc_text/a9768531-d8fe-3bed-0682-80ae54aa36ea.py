import cadquery as cq
shaft_length = 80.0
step_length = 30.0
step_radius = step_diameter / 2.0
shaft_diameter = 30.0
key_slot_width = 8.0
key_slot_depth = 4.0
key_slot_length = shaft_length - 20.0
chamfer_distance = 1.0
outer_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(shaft_length, 0)
    .lineTo(shaft_length, step_length - step_length)
    .lineTo(step_radius, step_length - step_length)
    .lineTo(step_radius, step_length)
    .lineTo(0, step_length)
    .close()
)
shaft_body = outer_profile.revolve()
shaft_body = shaft_body.faces(">Z").edges().chamfer(chamfer_distance)
key_slot = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(key_slot_width, key_slot_depth)
    .extrude(key_slot_length)
)
shaft_body = shaft_body.cut(key_slot)
key_slot = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(key_slot_diameter / 2.0)
    .extrude(key_slot_length)
)
shaft_body = shaft_body.cut(key_slot)
result = shaft_body
