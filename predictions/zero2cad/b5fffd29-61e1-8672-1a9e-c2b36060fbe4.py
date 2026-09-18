import cadquery as cq

# Parameters
plate_length = 80.0
plate_width = 60.0
plate_thickness = 10.0
pocket_length = 40.0
pocket_width = 30.0
pocket_depth = 5.0
bearing_diameter = 30.0
bearing_clearance = 0.5
bearing_hole_diameter = bearing_diameter + bearing_clearance
mount_hole_diameter = 4.0
mount_hole_offset = 15.0
chamfer_size = 1.0

# Base plate with composite sketch (rectangle + central circle)
base = (
    cq.Workplane("XY")
    .sketch()
    .rect(plate_length, plate_width)
    .circle(bearing_diameter / 2)
    .finalize()
    .extrude(plate_thickness)
)

# Recessed pocket on top surface
pocket = (
    base.faces(">Z").workplane()
    .rect(pocket_width, pocket_length)
    .cutBlind(-pocket_depth)
)

# Bearing clearance hole through the plate (centered)
bearing_hole = (
    pocket.faces(">Z").workplane()
    .hole(bearing_hole_diameter)
)

# Mounting holes pattern (four corners)
mount_holes = (
    bearing_hole.faces(">Z").workplane()
    .pushPoints([
        (mount_hole_offset, mount_hole_offset),
        (-mount_hole_offset, mount_hole_offset),
        (-mount_hole_offset, -mount_hole_offset),
        (mount_hole_offset, -mount_hole_offset),
    ])
    .hole(mount_hole_diameter)
)

# Chamfer top edges for safety
result = (
    mount_holes.faces(">Z").edges()
    .chamfer(chamfer_size)
)
