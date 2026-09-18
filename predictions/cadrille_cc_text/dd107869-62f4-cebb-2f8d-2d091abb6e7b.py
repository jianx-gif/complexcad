import cadquery as cq
base_plate_width = 60.0
base_plate_depth = 40.0
base_plate_thickness = 8.0
base_fillet_radius = 3.0
arm_length = 30.0
arm_width = 12.0
arm_fillet_radius = 0.5
mount_hole_diameter = 4.0
mount_hole_spacing = 30.0
arm_fillet_radius = 0.5
arm_width = 12.0
arm_plate_thickness = base_plate_thickness
base_plate = (
    cq.Workplane("XY")
    .rect(base_plate_width, base_plate_depth)
    .extrude(base_plate_thickness)
)
base_plate = (
    base_plate
    .faces(">Z")
    .workplane()
    .rect(arm_width, arm_length)
    .cutBlind(-arm_width)
)
base_plate = (
    base_plate
    .faces(">Z")
    .workplane()
    .rect(arm_width, arm_length)
    .extrude(arm_width)
)
base_plate = (
    base_plate
    .faces(">Z")
    .workplane()
    .rect(arm_width, arm_length)
    .cutBlind(-arm_width)
)
base_plate = (
    base_plate
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(mount_hole_diameter / 2)
    .cutBlind(-arm_width)
)
base_plate = (
    base_plate
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(mount_hole_spacing, mount_hole_spacing)
    .cutBlind(-arm_width)
)
result = base_plate.union(base_plate)
