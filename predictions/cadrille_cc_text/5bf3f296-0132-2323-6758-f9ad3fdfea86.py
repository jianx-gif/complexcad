import cadquery as cq
circle_diameter = 40.0
rect_width = 60.0
rect_height = 30.0
rect_thickness = 5.0
fillet_radius = 3.0
side_hole_diameter = 8.0
side_hole_offset = 20.0
boss_diameter = 12.0
boss_height = 6.0
pocket_width = 30.0
pocket_depth = 10.0
pocket_depth = 15.0
pocket_angle = 90.0
boss_radius = boss_diameter / 2.0
boss_height = 6.0
result = (
    cq.Workplane("XY")
    .circle(circle_diameter / 2.0)
    .workplane(offset=rect_height)
    .circle(boss_radius)
    .loft(combine=True)
    .workplane(offset=rect_height)
    .center(boss_radius, 0)
    .rect(boss_height, rib_length)
    .loft(combine=True)
    .edges("|Z")
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .center(boss_radius - side_hole_offset, 0)
    .hole(side_hole_diameter)
    .center(boss_radius - side_hole_offset, 0)
    .circle(boss_radius)
    .cutBlind(-pocket_depth)
    .workplane(offset=rect_height)
    .center(boss_radius - side_hole_offset, 0)
    .hole(boss_diameter)
    .center(boss_radius + side_hole_offset, 0)
    .hole(boss_diameter)
    .center(boss_radius + side_hole_offset, 0)
    .rect(pocket_width, pocket_depth)
    .cutBlind(-pocket_depth)
)
