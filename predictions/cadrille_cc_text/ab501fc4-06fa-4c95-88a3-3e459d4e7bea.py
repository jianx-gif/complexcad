import cadquery as cq
outer_diameter = 80.0
inner_diameter = 60.0
rim_height = 8.0
boss_radius = 10.0
boss_height = 12.0
boss_radius = 12.0
mount_hole_diameter = 8.0
mount_hole_offset = 15.0
vent_radius = 5.0
vent_circle_radius = 30.0
vent_count = 8
vent_circle_radius = 30.0
vent_radius = boss_radius
base_plate_thickness = 2.0
base_plate = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(rim_height)
)
boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_height)
)
boss = base_plate.cut(boss)
boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_height)
)
boss = boss.cut(boss)
vent_radius = outer_diameter / 2 - mount_hole_offset
vent_radius = outer_diameter / 2 - mount_hole_offset
vent = (
    cq.Workplane("XY")
    .circle(vent_radius)
    .extrude(vent_radius)
    .translate((0, 0, vent_radius))
)
vent = vent.cut(vent)
vent = vent.edges().chamfer(0.5)
result = base_plate.union(vent)
