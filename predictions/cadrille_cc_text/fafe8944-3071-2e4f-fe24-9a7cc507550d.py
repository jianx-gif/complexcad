import cadquery as cq
outer_length = 80.0
outer_width = 50.0
outer_height = 20.0
wall_thickness = 2.0
recess_length = 40.0
recess_width = 30.0
recess_depth = 5.0
hole_diameter = 2.0
hole_pitch_x = 12.0
hole_pitch_y = 12.0
hole_rows = 2
hole_cols = 3
chamfer_dist = 0.5
rib_height = 12.0
rib_width = 4.0
rib_thickness = 2.0
result = (
    cq.Workplane("XY")
    .box(outer_length, outer_width, outer_height, centered=(True, True, False))
    .faces(">Z")
    .workplane()
    .rect(recess_length, recess_width)
    .cutBlind(-recess_depth)
    .faces(">Z")
    .workplane()
    .rect(recess_length - 2 * wall_thickness, recess_width - 2 * wall_thickness)
    .cutBlind(-recess_depth)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-hole_cols - 1, hole_cols - 1),
        (hole_cols - 1, hole_cols - 1),
        (-hole_cols - 1, hole_cols - 1),
    ])
    .hole(hole_diameter)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (hole_cols - 1, hole_cols - 1),
        (-hole_cols - 1, hole_cols - 1),
        (hole_cols - 1, hole_cols - 1),
    ])
    .hole(hole_diameter)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (hole_cols - 1, hole_cols - 1),
        (-hole_cols - 1, hole_cols - 1),
        (hole_cols - 1, hole_cols - 1),
    ])
    .hole(hole_diameter)
)
