import cadquery as cq

# Parameters
base_width = 60.0
base_depth = 40.0
base_thickness = 8.0
base_corner_radius = 3.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
arm_length = 30.0
arm_width = 12.0
arm_thickness = base_thickness
hinge_pin_diameter = 4.0
hinge_pin_length = base_thickness + arm_length
slot_width = 6.0
slot_height = 10.0
slot_depth = base_thickness
chamfer_distance = 0.5

# Base plate with rounded corners
base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(base_corner_radius)
)

# Mounting holes on top face
base = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
    .hole(mount_hole_diameter)
)

# Central slot for cable routing
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_height)
    .cutBlind(-slot_depth)
)

# Hinge pin (cylinder along X axis)
pin = (
    cq.Workplane("YZ")
    .center(0, 0)
    .circle(hinge_pin_diameter/2)
    .extrude(hinge_pin_length)
)

# Arm on +Y side
arm_pos = (
    cq.Workplane("XY")
    .center(0, base_depth/2 + arm_width/2)
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
    .translate((0, 0, base_thickness))
)

# Arm on -Y side
arm_neg = (
    cq.Workplane("XY")
    .center(0, -(base_depth/2 + arm_width/2))
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
    .translate((0, 0, base_thickness))
)

# Assemble all parts
result = base.union(pin).union(arm_pos).union(arm_neg)

# Chamfer outer edges of arms for safety
result = (
    result
    .edges("(>Y or <Y) and >Z")
    .chamfer(chamfer_distance)
)
