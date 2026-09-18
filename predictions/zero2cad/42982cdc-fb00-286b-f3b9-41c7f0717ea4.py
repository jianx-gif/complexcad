import cadquery as cq

# Parameters
arm_length = 80.0
circle_diameter = 20.0
rect_width = 40.0
rect_height = 15.0
boss_diameter = 12.0
boss_height = 10.0
chamfer_distance = 2.0
hole_diameter = 6.0
mount_hole_diameter = 4.0
mount_hole_spacing = 30.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 4.0
slot_width = 8.0
slot_length = 20.0
slot_depth = 10.0

# Base lofted arm between circle and rectangle
base = (
    cq.Workplane("XY")
    .circle(circle_diameter / 2)
    .workplane(offset=arm_length)
    .rect(rect_width, rect_height)
    .loft()
)

# Central boss at mid-length
boss = (
    cq.Workplane("XY")
    .workplane(offset=arm_length / 2)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# Combine base and boss
result = base.union(boss)

# Through hole along Z axis
result = result.faces(">Z").workplane().hole(hole_diameter)

# Chamfer on the rectangular end face
result = result.faces(">Z").edges().chamfer(chamfer_distance)

# Mounting holes on rectangular end face
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing / 2, 0), (mount_hole_spacing / 2, 0)])
    .hole(mount_hole_diameter)
)

# Reinforcing rib on side of arm
rib = (
    cq.Workplane("XZ")
    .workplane(offset=arm_length / 4)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
result = result.union(rib)

# Slot cut on side of arm
slot = (
    cq.Workplane("YZ")
    .workplane(offset=arm_length / 2)
    .rect(slot_width, slot_length)
    .extrude(slot_depth)
)
result = result.cut(slot)
