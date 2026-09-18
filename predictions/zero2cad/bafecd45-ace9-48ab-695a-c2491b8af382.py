import cadquery as cq

# Parameters
arm_length = 80.0
arm_width = 20.0
arm_thickness = 8.0
flange_length = 15.0
flange_width = 25.0
slot_length = 30.0
slot_width = 8.0
slot_offset = 10.0
hole_diameter = 6.0
hole_depth = 4.0
chamfer_size = 1.0
rib_width = 5.0
rib_height = 4.0
rib_spacing = 12.0
mount_hole_dia = 4.0
mount_hole_offset = 5.0

# Base profile with flange
profile = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (arm_length, 0),
        (arm_length, arm_width),
        (arm_length, arm_width + flange_width),
        (arm_length - flange_length, arm_width + flange_width),
        (arm_length - flange_length, arm_width),
        (0, arm_width),
        (0, 0),
    ])
    .close()
)

# Extrude to create solid
result = profile.extrude(arm_thickness)

# Slot cut through the arm (centered along length)
slot_center_x = arm_length / 2.0
slot_center_y = arm_width / 2.0
result = (
    result.faces(">Z")
    .workplane()
    .center(slot_center_x, slot_center_y)
    .rect(slot_length, slot_width)
    .cutBlind(-arm_thickness)
)

# Blind hole in flange (centered on flange region)
hole_center_x = arm_length - flange_length / 2.0
hole_center_y = arm_width + flange_width / 2.0
result = (
    result.faces(">Z")
    .workplane()
    .center(hole_center_x, hole_center_y)
    .hole(hole_diameter, depth=hole_depth)
)

# Chamfer outer edges for safety
result = result.edges().chamfer(chamfer_size)

# Add ribs on underside for stiffness (patterned along length)
rib_count = int((arm_length - 2 * mount_hole_offset) // rib_spacing)
for i in range(rib_count):
    rib_x = mount_hole_offset + i * rib_spacing
    rib = (
        cq.Workplane("XY")
        .center(rib_x, arm_width / 2.0)
        .rect(rib_width, rib_height)
        .extrude(-rib_height)
    )
    result = result.union(rib)

# Mounting holes on the base (two holes symmetric about center)
mount_y = arm_width / 2.0
mount_x1 = mount_hole_offset
mount_x2 = arm_length - mount_hole_offset
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(mount_x1, mount_y), (mount_x2, mount_y)])
    .hole(mount_hole_dia)
)
