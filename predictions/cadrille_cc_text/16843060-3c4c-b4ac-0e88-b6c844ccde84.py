import cadquery as cq
plate_width = 80.0
plate_depth = 60.0
plate_thickness = 6.0
edge_fillet_radius = 8.0
boss_width = 20.0
boss_height = 4.0
boss_depth = 15.0
hole_diameter = 6.0
hole_depth = 4.0
hole_spacing_x = 30.0
hole_spacing_y = 25.0
hole_rows = 2
hole_cols = 3
edge_chamfer = 1.0
boss_fillet = 2.0
boss_depth = 15.0
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_depth, plate_thickness)
    .edges("|Z").fillet(edge_fillet_radius)
    .faces(">Z").workplane()
    .rect(boss_width, boss_depth)
    .extrude(boss_height)
    .faces(">Z").workplane()
    .rect(boss_width - 2 * edge_fillet_radius, boss_depth - 2 * edge_fillet_radius)
    .vertices()
    .hole(hole_diameter)
    .faces(">Z").workplane()
    .pushPoints([
        (hole_cols - 1) * hole_spacing_x, hole_spacing_y * hole_spacing_y)
        for i in range(hole_cols)
    ])
    .hole(hole_diameter)
)
