import cadquery as cq

# Parameters
bracket_length = 80.0
bracket_width = 50.0
bracket_thickness = 8.0
rib_height = 20.0
rib_width = 6.0
rib_spacing = 30.0
counterbore_diameter = 12.0
counterbore_cbore_diameter = 20.0
counterbore_depth = 4.0
mount_hole_diameter = 5.0
mount_hole_spacing = 40.0
mount_hole_offset = 10.0
chamfer_size = 1.0
slot_width = 6.0
slot_length = 20.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

# Side slot for cable routing (cut through thickness)
base = (
    base.faces("<Z")
    .workplane()
    .center(-bracket_length/2 + slot_length/2, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-bracket_thickness)
)

# Counterbore hole at centre of top face
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .cboreHole(counterbore_diameter, counterbore_cbore_diameter, counterbore_depth)
)

# Mounting holes pattern on top face
mount_points = [
    (-mount_hole_spacing/2, -mount_hole_offset),
    (mount_hole_spacing/2, -mount_hole_offset),
    (-mount_hole_spacing/2, mount_hole_offset),
    (mount_hole_spacing/2, mount_hole_offset),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)

# Double ribs on top face
rib1 = (
    base.faces(">Z")
    .workplane()
    .center(-rib_spacing/2, 0)
    .rect(rib_width, bracket_width - 2*mount_hole_offset)
    .extrude(rib_height)
)
rib2 = (
    base.faces(">Z")
    .workplane()
    .center(rib_spacing/2, 0)
    .rect(rib_width, bracket_width - 2*mount_hole_offset)
    .extrude(rib_height)
)

# Combine base and ribs
result = base.union(rib1).union(rib2)

# Chamfer outer vertical edges for safety
result = result.edges("|Z").chamfer(chamfer_size)
