import cadquery as cq
arm_length = 80.0
outer_radius = 20.0
inner_radius = 12.0
boss_height = 15.0
boss_radius = 10.0
chamfer_dist = 2.0
mount_hole_diameter = 5.0
mount_hole_offset = 20.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
rib_offset_z = 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(arm_length)
)
boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_height)
    .translate((0, 0, arm_length - boss_height))
)
base = base.union(boss)
boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_height)
    .translate((0, 0, arm_length - boss_height))
)
base = base.cut(boss)
base = base.edges().chamfer(chamfer_dist)
rib = (
    cq.Workplane("XY")
    .circle(rib_width / 2)
    .extrude(rib_thickness)
    .translate((0, 0, arm_length - rib_thickness))
)
base = base.union(rib)
base = base.faces(">Z").edges().chamfer(chamfer_dist)
result = base
