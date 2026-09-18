import cadquery as cq
leg_length_x = 80.0
leg_length_y = 60.0
thickness = 15.0
boss_width = 12.0
boss_height = 20.0
boss_depth = 12.0
hole_diameter = 10.0
hole_clearance = 5.0
fillet_radius = 5.0
chamfer_dist = 1.0
mount_hole_dia = 5.0
mount_hole_count = 4
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_length_x, 0),
        (leg_length_x, thickness),
        (thickness, thickness),
        (thickness, leg_length_y),
        (0, leg_length_y),
        (0, 0),
    ])
    .close()
    .extrude(thickness)
)
boss = (
    base.faces(">Z")
    .workplane()
    .center(leg_length_x - boss_width/2, leg_length_y - boss_height/2)
    .rect(boss_width, boss_height)
    .extrude(boss_depth)
)
boss = (
    boss.faces(">Z")
    .workplane()
    .center(leg_length_x - boss_width/2, leg_length_y - boss_height/2)
    .hole(hole_diameter)
)
result = (
    boss.faces(">Z")
    .workplane()
    .center(leg_length_x - leg_length/2, leg_length_y - leg_length/2)
    .hole(mount_hole_dia)
)
