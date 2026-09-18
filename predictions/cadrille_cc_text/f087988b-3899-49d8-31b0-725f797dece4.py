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
base = (
    cq.Workplane("XY")
    .circle(plate_outer_diameter / 2)
    .circle(boss_diameter / 2)
    .extrude(plate_thickness)
)
boss = (
    cq.Workplane("XY")
    .circle(boss_diameter / 2)
    .extrude(boss_height)
    .translate((0, 0, plate_thickness))
)
plate_with_boss = base.union(boss)
plate_with_holes = (
    plate_with_holes.faces(">Z").workplane()
    .circle(mounting_hole_diameter / 2)
    .cutBlind(-mounting_hole_offset)
)
plate_with_holes = (
    plate_with_holes.faces(">Z").workplane()
    .polarArray(radius=mounting_hole_offset, count=mounting_hole_offset, startAngle=0, angle=360)
    .circle(mounting_hole_diameter / 2)
    .cutBlind(-mounting_hole_depth)
)
result = plate_with_holes.edges().chamfer(chamfer_size)
