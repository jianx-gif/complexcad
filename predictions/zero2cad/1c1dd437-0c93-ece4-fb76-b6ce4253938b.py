import cadquery as cq

# Parameters
base_diameter = 60.0
step1_diameter = 40.0
step2_diameter = 20.0
base_height = 30.0
step1_height = 30.0
step2_height = 20.0
fillet_radius = 2.0
counterbore_diameter = 8.0
counterbore_depth = 5.0
mount_hole_diameter = 5.0
mount_hole_offset = 12.0
slot_width = 6.0
slot_length = 20.0
slot_depth = 10.0

# Derived dimensions
total_height = base_height + step1_height + step2_height
step1_radius = step1_diameter / 2.0
step2_radius = step2_diameter / 2.0

# Base stepped cylinder via revolve of composite profile
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_diameter / 2.0, 0)
    .lineTo(base_diameter / 2.0, base_height)
    .lineTo(step1_diameter / 2.0, base_height)
    .lineTo(step1_diameter / 2.0, base_height + step1_height)
    .lineTo(step2_diameter / 2.0, base_height + step1_height)
    .lineTo(step2_diameter / 2.0, total_height)
    .lineTo(0, total_height)
    .close()
)

result = profile.revolve()

# Fillet all edges for smooth transition
result = result.edges().fillet(fillet_radius)

# Counterbore on top face
result = (
    result.faces(">Z")
    .workplane()
    .cboreHole(counterbore_diameter, counterbore_diameter * 1.5, counterbore_depth)
)

# Mounting holes on bottom face (four cardinal points)
mount_points = [
    (mount_hole_offset, 0),
    (-mount_hole_offset, 0),
    (0, mount_hole_offset),
    (0, -mount_hole_offset),
]
result = (
    result.faces("<Z")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)

# Slot on side of step2 region (cutting a rectangular pocket)
slot_center_z = base_height + step1_height + step2_height / 2.0
result = (
    result.workplane(offset=slot_center_z)
    .center(step2_radius, 0)
    .rect(slot_width, slot_length)
    .cutBlind(-slot_depth)
)
