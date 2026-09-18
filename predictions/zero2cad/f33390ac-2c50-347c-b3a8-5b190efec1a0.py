import cadquery as cq

arm_length = 80.0
arm_width = 12.0
arm_thickness = 8.0
sweep_height = 6.0
boss_diameter = 12.0
boss_height = 10.0
hole_diameter = 3.0
mount_hole_diameter = 3.0
mount_hole_spacing = 30.0
rib_width = 4.0
rib_height = 2.0
rib_spacing = 15.0

path = (
    cq.Workplane("XZ")
    .spline([
        (0, 0),
        (arm_length * 0.3, sweep_height * 0.5),
        (arm_length, 0)
    ])
    .wire()
)

arm = (
    cq.Workplane("XY")
    .rect(arm_width, arm_thickness)
    .sweep(path, makeSolid=True)
)

boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

result = arm.union(boss)

through_hole = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(hole_diameter / 2)
    .extrude(arm_length + boss_height + 2)
)
result = result.cut(through_hole)

mount_hole = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(mount_hole_diameter / 2)
    .extrude(arm_thickness + 2)
)
mount1 = mount_hole.translate((arm_length * 0.25, 0, 0))
mount2 = mount_hole.translate((arm_length * 0.75, 0, 0))
result = result.cut(mount1).cut(mount2)

rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(arm_thickness / 2)
)
num_ribs = int(arm_length // rib_spacing)
for i in range(num_ribs):
    x_pos = (i + 0.5) * rib_spacing
    rib_instance = rib.translate((x_pos, 0, 0))
    result = result.union(rib_instance)
