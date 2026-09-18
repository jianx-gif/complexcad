import cadquery as cq

# Dimensions
base_length = 80.0
base_width = 60.0
base_thickness = 5.0
raised_radius = 12.0
raised_height = 20.0
vent_slot_length = 30.0
vent_slot_width = 5.0
vent_slot_count = 4
vent_slot_spacing = 12.0
thread_turns = 11
thread_profile_height = 2.0
thread_profile_width = 3.0
thread_offset_radius = raised_radius + 0.5 * thread_profile_width
chamfer_distance = 0.5

# Base plate with vent slots
base_plate = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)

for i in range(vent_slot_count):
    slot_y = -((vent_slot_count - 1) / 2.0 - i) * vent_slot_spacing
    base_plate = (
        base_plate.faces(">Z")
        .workplane()
        .center(0, slot_y)
        .rect(vent_slot_width, vent_slot_length)
        .cutBlind(-base_thickness * 0.9)
    )

# Raised central cylinder
cylinder = (
    cq.Workplane("XY")
    .circle(raised_radius)
    .extrude(raised_height)
    .translate((0, 0, base_thickness))
)

cylinder = cylinder.faces(">Z").edges().chamfer(chamfer_distance)

# Thread profile offset from axis
thread_profile = (
    cq.Workplane("XY")
    .moveTo(thread_offset_radius, 0)
    .lineTo(thread_offset_radius + thread_profile_width / 2, thread_profile_height / 2)
    .lineTo(thread_offset_radius + thread_profile_width / 2, -thread_profile_height / 2)
    .close()
)

thread = (
    thread_profile
    .twistExtrude(raised_height, 360 * thread_turns)
    .translate((0, 0, base_thickness))
)

worm_body = cylinder.union(thread)

result = base_plate.union(worm_body)
