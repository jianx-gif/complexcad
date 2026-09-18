import cadquery as cq

# Parameters
plate_width = 80.0
plate_height = 60.0
plate_thickness = 8.0
slot_width = 30.0
slot_height = 10.0
central_hole_diameter = 12.0
mount_hole_diameter = 5.0
mount_cbore_diameter = 8.0
mount_cbore_depth = 2.0
mount_offset = 10.0
fillet_radius = 1.5

# Base plate with filleted vertical edges
result = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# Central slot cut through the plate
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(slot_width, slot_height)
    .cutBlind(-plate_thickness)
)

# Central through hole
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(central_hole_diameter)
)

# Mounting holes pattern (three holes)
mount_points = [
    (-plate_width/2 + mount_offset, plate_height/2 - mount_offset),
    (plate_width/2 - mount_offset, plate_height/2 - mount_offset),
    (0, -plate_height/2 + mount_offset)
]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(mount_points)
    .cboreHole(mount_hole_diameter, mount_cbore_diameter, mount_cbore_depth)
)
