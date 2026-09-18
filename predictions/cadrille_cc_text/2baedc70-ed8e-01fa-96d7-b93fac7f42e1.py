import cadquery as cq
arm_length = 80.0
step_height = 20.0
step_radius = 15.0
mid_radius = 10.0
boss_width = 30.0
boss_height = 8.0
boss_thickness = 5.0
tip_radius = 10.0
hole_diameter = 4.0
hole_offset = 12.0
fillet_radius = 2.0
chamfer_dist = 1.0
outer = (
    cq.Workplane("XY")
    .circle(arm_length)
    .extrude(arm_length)
)
inner = (
    cq.Workplane("XY")
    .circle(boss_width)
    .extrude(boss_height)
    .translate((0, 0, arm_length - boss_height))
)
base = outer.union(inner)
boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(boss_width / 2)
    .extrude(boss_height)
)
boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(boss_width / 2)
    .extrude(boss_height)
)
result = base.union(boss)
result = result.edges("|Z").fillet(fillet_radius)
result = result.edges("|Z").chamfer(chamfer_dist)
