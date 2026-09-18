import cadquery as cq
body_radius = 45.0
body_height = 70.0
wall_thickness = 3.0
boss_radius = 15.0
boss_height = 12.0
keyway_width = 6.0
keyway_depth = 8.0
keyway_depth = 3.0
mount_hole_diameter = 4.0
mount_hole_spacing = 20.0
vent_hole_diameter = 12.0
vent_pitch = 12.0
vent_hole_count = 4
vent_hole_spacing = 20.0
chamfer_distance = 1.0
boss_radius = 15.0
boss_height = 30.0
body = (
    cq.Workplane("XY")
    .circle(body_radius)
    .workplane(offset=body_height)
    .circle(boss_radius)
    .workplane(offset=body_height)
    .circle(boss_radius)
    .cutBlind(-body_height)
)
keyway = (
    cq.Workplane("XY")
    .workplane(offset=body_height)
    .center(0, 0)
    .rect(keyway_width, keyway_depth)
    .cutBlind(-keyway_depth)
)
result = body.union(keyway)
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(mount_hole_diameter)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(vent_hole_diameter / 2)
    .cutBlind(-vent_hole_depth)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(vent_hole_diameter / 2)
    .cutBlind(-vent_hole_depth)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(keyway_width, keyway_depth)
    .cutBlind(-keyway_depth)
)
