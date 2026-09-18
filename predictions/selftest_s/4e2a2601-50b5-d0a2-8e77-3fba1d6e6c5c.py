import cadquery as cq

long_leg = 80.0
short_leg = 50.0
leg_width = 20.0
thickness = 8.0
slot_width = 8.0
slot_depth = thickness * 0.75
slot_spacing = 20.0
num_slots = 3
hole_diameter = 6.0
csk_diameter = 12.0
csk_angle = 82.0
hole_spacing = 30.0
num_holes = 3
chamfer_size = 1.0

profile = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (long_leg, 0),
        (long_leg, leg_width),
        (leg_width, leg_width),
        (leg_width, short_leg),
        (0, short_leg),
        (0, 0),
    ])
    .close()
)

result = profile.extrude(thickness)

for i in range(num_slots):
    slot_center_y = (i + 0.5) * slot_spacing
    result = (
        result.faces("<X").workplane()
        .center(0, slot_center_y)
        .rect(slot_width, thickness)
        .cutBlind(-slot_depth)
    )

hole_positions = []
start_x = leg_width + hole_spacing
for i in range(num_holes):
    x = start_x + i * hole_spacing
    y = leg_width / 2.0
    hole_positions.append((x, y))

result = (
    result.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)

result = result.edges("|Z").chamfer(chamfer_size)
