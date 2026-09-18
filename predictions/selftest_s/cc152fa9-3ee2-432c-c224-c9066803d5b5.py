import cadquery as cq
arm_length = 80
max_radius = 10
grip_start = 30
grip_length = 30
grip_radius = 12
fillet_radius = 2
cable_hole_diameter = 5
cable_hole_offset = 8
mount_flange_radius = 20
mount_flange_thickness = 5
mount_hole_diameter = 4
mount_hole_spacing = 30
knurl_pitch = 2
knurl_depth = 0.8
knurl_bump_radius = knurl_depth/2
knurl_bump_height = 2
num_circ = 12
# Revolve profile to create arm
arm = (
    cq.Workplane("YZ")
    .polyline([
        (0, max_radius),
        (grip_start, max_radius),
        (grip_start + grip_length, grip_radius),
        (arm_length, grip_radius),
        (arm_length, 0),
        (0, 0),
    ])
    .close()
    .revolve(360)
)
arm = arm.edges().fillet(fillet_radius)
# Mounting flange at root (plane Y=0, extrude negative Y)
flange = (
    cq.Workplane("XZ")
    .center(0, 0)
    .circle(mount_flange_radius)
    .extrude(-mount_flange_thickness)
)
for x in (-mount_hole_spacing/2, mount_hole_spacing/2):
    flange = flange.cut(
        cq.Workplane("XZ")
        .center(x, 0)
        .circle(mount_hole_diameter/2)
        .extrude(-mount_flange_thickness)
    )
result = arm.union(flange)
# Knurl bumps along grip region
num_axial = int(grip_length / knurl_pitch)
for i in range(num_axial):
    y_pos = grip_start + i * knurl_pitch + knurl_pitch/2
    bumps = (
        cq.Workplane("XY")
        .center(0, y_pos)
        .polarArray(radius=grip_radius - knurl_depth, startAngle=0, angle=360, count=num_circ)
        .circle(knurl_bump_radius)
        .extrude(knurl_bump_height)
        .translate((0, 0, knurl_bump_height/2))
    )
    result = result.union(bumps)
# Cable through‑hole near distal end (axis Y)
cable_hole_center_y = arm_length - 10
cable_hole = (
    cq.Workplane("XZ")
    .center(cable_hole_offset, cable_hole_center_y)
    .circle(cable_hole_diameter/2)
    .extrude(arm_length + 20, both=True)
)
result = result.cut(cable_hole)
