import cadquery as cq
base_width = 80.0
base_depth = 60.0
base_thickness = 12.0
base_corner_radius = 5.0
base_corner_radius = base_depth - 2.0
boss_diameter = 30.0
boss_height = 20.0
insert_hole_diameter = 6.0
insert_hole_depth = 15.0
mount_hole_dia = 5.0
mount_hole_spacing_x = 60.0
mount_hole_spacing_y = 40.0
mount_hole_rows = 2
mount_hole_cols = 3
mount_hole_cols = 3
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(base_width, 0)
    .lineTo(base_width, base_depth)
    .lineTo(boss_diameter/2, base_depth)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_depth + insert_hole_diameter)
    .lineTo(boss_diameter/2, base_depth + insert_hole_diameter)
    .lineTo(boss_diameter/