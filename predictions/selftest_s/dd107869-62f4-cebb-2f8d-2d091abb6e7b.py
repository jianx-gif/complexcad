import cadquery as cq

# Parameters
base_plate_width = 60.0
base_plate_depth = 40.0
base_plate_thickness = 8.0
base_fillet_radius = 3.0
hinge_pin_diameter = 4.0
hinge_pin_length = 80.0
hinge_gap_width = 6.0
hinge_gap_height = base_plate_thickness + 2.0
arm_length = 30.0
arm_width = 12.0
arm_thickness = base_plate_thickness
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
arm_fillet_radius = 0.5

# Base plate with filleted corners, tag top edges for later fillet
base_plate = (
    cq.Workplane("XY")
    .rect(base_plate_width, base_plate_depth)
    .extrude(base_plate_thickness)
    .edges("|Z")
    .tag("base_top_edges")
    .end()
)

# Hinge pin oriented along X axis, passing through centre of base
hinge_pin = (
    cq.Workplane("YZ")
    .center(0, 0)
    .circle(hinge_pin_diameter / 2)
    .extrude(hinge_pin_length)
    .translate((0, 0, base_plate_thickness / 2))
)

# Front arm attached to the front edge of the base
front_arm = (
    cq.Workplane("XY")
    .center(0, base_plate_depth / 2 + arm_width / 2)
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
    .translate((0, 0, base_plate_thickness - 0.01))
)

# Back arm attached to the rear edge of the base
back_arm = (
    cq.Workplane("XY")
    .center(0, -base_plate_depth / 2 - arm_width / 2)
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
    .translate((0, 0, base_plate_thickness - 0.01))
)

# Assemble base, pin, and arms
assembly = (
    cq.Workplane("XY")
    .union(base_plate)
    .union(hinge_pin)
    .union(front_arm)
    .union(back_arm)
)

# Split hinge gap cut through the centre of the assembly
assembly = (
    assembly
    .workplane(offset=base_plate_thickness / 2)
    .center(0, 0)
    .rect(hinge_gap_width, hinge_gap_height)
    .cutBlind(-base_plate_thickness - 0.1)
)

# Mounting holes on top surface, symmetric about centre
assembly = (
    assembly
    .faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing / 2, 0), (mount_hole_spacing / 2, 0)])
    .hole(mount_hole_diameter)
)

# Fillet base top edges
assembly = (
    assembly
    .edges(tag = "base_top_edges")
    .fillet(base_fillet_radius)
)

# Fillet top edges of arms for safety
assembly = (
    assembly
    .edges(">>Z and |Y")
    .fillet(arm_fillet_radius)
)

result = assembly