import cadquery as cq

arm_length = 30.0
arm_width = 12.0
base_thickness = 8.0
web_extra_thickness = 4.0
web_width = 20.0
slot_width = 6.0
slot_length = 12.0
chamfer_size = 0.6

vertical_bar = (
    cq.Workplane("XY")
    .rect(arm_width, 2 * arm_length + arm_width)
    .extrude(base_thickness)
)

horizontal_bar = (
    cq.Workplane("XY")
    .rect(2 * arm_length + arm_width, arm_width)
    .extrude(base_thickness)
)

base = vertical_bar.union(horizontal_bar)

central_web = (
    cq.Workplane("XY")
    .rect(web_width, web_width)
    .extrude(base_thickness + web_extra_thickness)
)

combined = base.union(central_web).edges("|Z").chamfer(chamfer_size).faces(">Z").tag("top")

slot_coords = [
    (0, 0.6 * arm_length),
    (0, -0.6 * arm_length),
    (0.6 * arm_length, 0),
    (-0.6 * arm_length, 0),
    (0.42 * arm_length, 0.42 * arm_length),
    (-0.42 * arm_length, -0.42 * arm_length),
]

result = combined
for x_offset, y_offset in slot_coords:
    result = (
        result.workplaneFromTagged("top")
        .center(x_offset, y_offset)
        .rect(slot_length, slot_width)
        .cutBlind(-base_thickness)
    )

result = result
