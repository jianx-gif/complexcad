import cadquery as cq

bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 5.0
wall_margin = 5.0
mount_hole_diameter = 5.0
mount_clearance = 6.0
mount_cbore_diameter = 8.0
mount_cbore_depth = 2.0
rib_thickness = 2.0
rib_spacing = 12.0
latch_arm_length = 30.0
latch_arm_width = 6.0
latch_fillet_radius = 0.8
pin_diameter = 4.0
pin_height = 6.0
pin_offset_x = 20.0
pin_offset_y = bracket_width/2 - 5.0
chamfer_dist = 0.3

base = (
    cq.Workplane("XY")
    .box(bracket_length, bracket_width, bracket_thickness, centered=(True, True, False))
)

mount_points = [
    (bracket_length/2 - 15, bracket_width/2 - 15),
    (bracket_length/2 - 15, -bracket_width/2 + 15),
    (-bracket_length/2 + 15, bracket_width/2 - 15),
    (-bracket_length/2 + 15, -bracket_width/2 + 15),
]

base = (
    base
    .faces('>Z')
    .workplane()
    .pushPoints(mount_points)
    .cboreHole(mount_clearance, mount_cbore_diameter, mount_cbore_depth)
)

rib_count = int((bracket_length - 2*wall_margin) // rib_spacing)
rib_positions = [(-bracket_length/2 + wall_margin + i * rib_spacing) for i in range(rib_count)]

ribs = cq.Workplane('XY')
for x_pos in rib_positions:
    ribs = ribs.union(
        cq.Workplane('XY')
        .center(x_pos, 0)
        .box(rib_thickness, bracket_width - 2*wall_margin, bracket_thickness, centered=(True, True, False))
    )

body = base.union(ribs)

latch = (
    cq.Workplane('XY')
    .center(bracket_length/2, 0)
    .rect(latch_arm_length, latch_arm_width)
    .extrude(bracket_thickness)
    .translate((0, bracket_width/2 + latch_arm_width/2, 0))
)

latch = latch.edges('|Z').fillet(latch_fillet_radius)

body = body.union(latch)

pin = (
    cq.Workplane('XY')
    .circle(pin_diameter/2)
    .extrude(pin_height)
)

pin1 = pin.translate((pin_offset_x, pin_offset_y, 0))
pin2 = pin.translate((pin_offset_x, -pin_offset_y, 0))

body = body.union(pin1).union(pin2)

result = body.faces('>Z').edges().chamfer(chamfer_dist)