import cadquery as cq

outer_length = 80.0
outer_width = 50.0
outer_height = 20.0
wall_thickness = 2.0
recess_length = 40.0
recess_width = 30.0
recess_depth = 5.0
hole_diameter = 2.0
hole_rows = 4
hole_cols = 5
hole_pitch_x = 12.0
hole_pitch_y = 12.0
chamfer_dist = 0.5
rib_height = 12.0
rib_thickness = 2.0
rib_width = 4.0

result = (
    cq.Workplane("XY")
    .box(outer_length, outer_width, outer_height, centered=(True, True, False))
    .faces(">Z or <Z")
    .shell(-wall_thickness)
    .faces(">Z")
    .workplane()
    .rect(recess_length, recess_width)
    .cutBlind(-recess_depth)
    .faces(">Z")
    .workplane()
    .rarray(hole_pitch_x, hole_pitch_y, hole_cols, hole_rows)
    .hole(hole_diameter)
    .edges("|Z")
    .chamfer(chamfer_dist)
    .faces(">X")
    .workplane()
    .rect(rib_height, rib_thickness)
    .extrude(rib_width, combine=True)
)
