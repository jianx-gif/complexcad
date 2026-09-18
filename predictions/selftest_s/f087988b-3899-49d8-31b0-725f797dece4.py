import cadquery as cq

plate_outer_diameter = 80.0
plate_thickness = 10.0
boss_diameter = 30.0
boss_height = 8.0
groove_width = 5.0
groove_depth = 2.0
mounting_hole_diameter = 8.0
mounting_hole_offset = 30.0
chamfer_size = 1.0

plate_outer_radius = plate_outer_diameter / 2.0
boss_radius = boss_diameter / 2.0

base_profile = (
    cq.Workplane("XZ")
    .moveTo(plate_outer_radius, 0)
    .lineTo(plate_outer_radius, plate_thickness)
    .lineTo(0, plate_thickness)
    .lineTo(0, 0)
    .close()
    .revolve(360)
)

boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(boss_radius)
    .extrude(boss_height)
    .translate((0, 0, plate_thickness))
)

plate_with_boss = base_profile.union(boss)

plate_with_groove = (
    plate_with_boss
    .faces(">Z")
    .workplane()
    .circle(boss_radius + groove_width)
    .circle(boss_radius)
    .cutBlind(-groove_depth)
)

holes = (
    plate_with_groove
    .faces("<Z")
    .workplane()
    .polarArray(radius=mounting_hole_offset, count=4, startAngle=0, angle=360)
    .circle(mounting_hole_diameter / 2.0)
    .cutBlind(plate_thickness + boss_height)
)

result = (
    holes
    .edges()
    .chamfer(chamfer_size)
)
