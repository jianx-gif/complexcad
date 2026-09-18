import cadquery as cq

block_length = 80.0
block_width = 50.0
block_thickness = 12.0
cylinder_dia = 30.0
cylinder_depth = 6.0
keyway_width = 12.0
keyway_length = 30.0
keyway_depth = 8.0
blind_hole_dia = 5.0
blind_hole_depth = 4.0
blind_rows = 2
blind_cols = 5
blind_spacing_x = 12.0
blind_spacing_y = 15.0
edge_fillet = 2.0
top_chamfer = 0.5

result = (
    cq.Workplane("XY")
    .box(block_length, block_width, block_thickness)
    .faces(">Z").workplane()
    .circle(cylinder_dia / 2)
    .cutBlind(cylinder_depth)
    .faces(">X").workplane()
    .rect(keyway_length, keyway_width)
    .cutBlind(keyway_depth)
    .faces(">Z").workplane()
    .rarray(blind_spacing_x, blind_spacing_y, blind_cols, blind_rows)
    .circle(blind_hole_dia / 2)
    .cutBlind(blind_hole_depth)
    .edges("|Z").fillet(edge_fillet)
    .faces(">Z").chamfer(top_chamfer)
)
