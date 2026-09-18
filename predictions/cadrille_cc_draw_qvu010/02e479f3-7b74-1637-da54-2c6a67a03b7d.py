import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
wall_thickness = 4.0
inner_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
boss_radius = 12.0
boss_height = 10.0
boss_depth = 6.0
chamfer_size = 1.0
mount_hole_dia = 5.0
mount_hole_offset = 10.0
mount_hole_count = 4
mount_hole_radius = outer_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(outer_diameter)
)
boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_height)
    .translate((0, 0, wall_thickness))
)
boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_height)
    .translate((0, 0, wall_thickness))
)
boss = boss.cut(boss)
boss = boss.faces(">Z").edges().chamfer(chamfer_size)
boss = boss.faces(">Z").workplane().hole(inner_radius * 2)
boss = boss.faces(">Z").workplane().circle(boss_radius).extrude(boss_height)
boss = boss.faces(">Z").workplane().circle(boss_radius).extrude(boss_height)
boss = boss.faces(">Z").workplane().circle(boss_radius).cutBlind(boss_height)
boss = boss.faces(">Z").workplane().circle(boss_radius).cutBlind(boss_height)
boss = boss.faces(">Z").workplane().circle(boss_radius).cutBlind(boss_height)
boss = boss.faces(">Z").workplane().polarArray(radius=mount_hole_radius, count=mount_hole_count, startAngle=0, angle=360).hole(mount_hole_dia)
boss = boss.faces(">Z").workplane().pushPoints(boss).hole(mount_hole_dia)
boss = boss.faces(">Z").edges().chamfer(chamfer_size)
result = boss
