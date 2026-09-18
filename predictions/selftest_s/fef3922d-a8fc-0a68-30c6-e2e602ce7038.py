import cadquery as cq

# Parameters
arm_length = 80.0
outer_radius = 20.0
inner_radius = 12.0
boss_radius = 10.0
boss_height = 15.0
chamfer_dist = 2.0
mount_hole_diameter = 5.0
mount_hole_offset = 20.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
rib_offset_z = -2.0

# Base lofted pivot arm
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .workplane(offset=arm_length)
    .circle(inner_radius)
    .loft()
)

# Central boss
boss = (
    cq.Workplane("XY")
    .workplane(offset=arm_length / 2)
    .circle(boss_radius)
    .extrude(boss_height)
    .translate((0, 0, -boss_height / 2))
)

# Combine base and boss
pivot = base.union(boss)

# Side mounting holes (two, opposite sides)
hole1 = (
    cq.Workplane("XY")
    .workplane(offset=arm_length / 4)
    .transformed(rotate=(0, 90, 0))
    .center(mount_hole_offset, 0)
    .circle(mount_hole_diameter / 2)
    .extrude(arm_length)
)

hole2 = (
    cq.Workplane("XY")
    .workplane(offset=3 * arm_length / 4)
    .transformed(rotate=(0, 90, 0))
    .center(-mount_hole_offset, 0)
    .circle(mount_hole_diameter / 2)
    .extrude(arm_length)
)

pivot = pivot.cut(hole1).cut(hole2)

# Reinforcement ribs on the lower side (negative Z)
rib = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .translate((0, 0, rib_offset_z))
)

pivot = pivot.union(rib)

# Chamfer outer edge (edges parallel to Z)
pivot = pivot.edges("|Z").chamfer(chamfer_dist)

result = pivot