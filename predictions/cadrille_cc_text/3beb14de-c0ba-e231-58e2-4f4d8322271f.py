import cadquery as cq
outer_width = 60.0
outer_depth = 40.0
total_height = 20.0
wall_thickness = 5.0
notch_width = 8.0
notch_height = 12.0
notch_offset = 12.0
boss_diameter = 12.0
boss_height = 4.0
boss_offset = 12.0
hole_diameter = 1.0
hole_spacing = 15.0
chamfer = 2.0
base = (
    cq.Workplane("XY")
    .rect(outer_width, outer_depth)
    .extrude(total_height)
)
notch = (
    cq.Workplane("XY")
    .center(0, 0)
    .polyline([
        (-notch_width/2, 0),
        (0, -notch_height),
        (notch_width/2, -notch_height),
        (notch_width/2, 0),
        (-notch_width/2, 0)
    ])
    .close()
    .extrude(total_height)
)
boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(boss_diameter/2)
    .extrude(boss_height)
)
boss = boss.cut(boss)
boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(notch_width, notch_depth)
    .extrude(total_height)
)
boss = boss.cut(boss)
boss = (
    boss.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
boss = boss.faces(">Z").edges().chamfer(chamfer)
result = boss
