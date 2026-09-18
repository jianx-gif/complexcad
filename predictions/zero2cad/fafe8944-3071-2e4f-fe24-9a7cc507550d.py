import cadquery as cq

outer_length = 80.0
outer_width = 50.0
outer_height = 20.0
wall_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 3.0
hole_spacing_x = 20.0
hole_spacing_y = 15.0
hole_rows = 2
hole_cols = 3
snap_tab_width = 12.0
snap_tab_thickness = 2.0
snap_tab_height = 4.0

result = (
    cq.Workplane("XY")
    .box(outer_length, outer_width, outer_height, centered=(True, True, False))
    .faces(">Z or <Z")
    .shell(-wall_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
    .faces(">Z")
    .workplane()
    .rarray(hole_spacing_x, hole_spacing_y, hole_cols, hole_rows)
    .hole(hole_diameter)
    .faces(">X")
    .workplane()
    .rect(snap_tab_width, snap_tab_thickness)
    .extrude(snap_tab_height)
)
