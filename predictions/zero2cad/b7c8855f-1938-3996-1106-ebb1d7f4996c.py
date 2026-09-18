import cadquery as cq

# Parameters
base_width = 70.0
base_depth = 30.0
base_thickness = 5.0
base_corner_radius = 3.0
mount_hole_diameter = 6.0
mount_hole_offset_y = 5.0

clip_arm_length = 25.0
clip_arm_width = 15.0
clip_arm_thickness = 4.0
clip_arm_fillet = 2.0
clip_arm_offset_y = -10.0

rib_width = 5.0
rib_height = 12.0
rib_offset_y = -15.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_thickness)
    .edges("|Z")
    .tag("base_edges")
    .end()
)

# Clip arm (rectangular block) with filleted vertical edges
clip_arm = (
    cq.Workplane("XY")
    .rect(clip_arm_length, clip_arm_width)
    .extrude(clip_arm_thickness)
    .edges("|Z")
    .fillet(clip_arm_fillet)
    .translate((0, clip_arm_offset_y, base_thickness))
)

# Reinforcing rib (rectangular block) positioned on underside of base
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(base_thickness)
    .translate((0, rib_offset_y, 0))
)

# Assemble components
result = base.union(clip_arm).union(rib)

# Mounting hole through base plate
result = (
    result
    .workplaneFromTagged("base_edges")
    .center(0, mount_hole_offset_y)
    .circle(mount_hole_diameter / 2)
    .cutThruAll()
)
