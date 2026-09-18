import cadquery as cq

channel_length = 80.0
channel_width = 40.0
channel_height = 30.0
wall_thickness = 3.0
fillet_radius = 2.0
chamfer_distance = 0.5
vent_width = 5.0
vent_length = 20.0
vent_count = 3
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 3

base = (
    cq.Workplane("XY")
    .box(channel_length, channel_width, channel_height, centered=(True, True, False))
    .shell(-wall_thickness)
    .edges("|Z and >Y")
    .fillet(fillet_radius)
    .edges(">Z and |X")
    .chamfer(chamfer_distance)
)

# Add vent slots on inner bottom face
vent_face = base.faces("<Z")
vent_pattern = (
    vent_face.workplane()
    .rarray(
        (channel_width - 2 * wall_thickness - vent_width) / (vent_count - 1),
        0,
        vent_count,
        1,
    )
    .rect(vent_width, vent_length)
    .cutBlind(-wall_thickness)
)

# Add mounting holes on side faces (+X and -X)
side_holes = (
    vent_pattern
    .faces(">X")
    .workplane()
    .rarray(0, (channel_length - 2 * wall_thickness - hole_spacing) / (hole_count - 1), 1, hole_count)
    .circle(hole_diameter / 2)
    .cutBlind(-wall_thickness)
    .faces("<X")
    .workplane()
    .rarray(0, (channel_length - 2 * wall_thickness - hole_spacing) / (hole_count - 1), 1, hole_count)
    .circle(hole_diameter / 2)
    .cutBlind(-wall_thickness)
)

result = side_holes