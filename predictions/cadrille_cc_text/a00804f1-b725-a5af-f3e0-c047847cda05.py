import cadquery as cq
outer_length = 80.0
outer_width = 40.0
outer_height = 30.0
wall_thickness = 3.0
chamfer_size = 1.5
hole_diameter = 4.0
hole_spacing = 30.0
hole_count = 6
hole_offset_x = outer_length / 2 - hole_spacing / 2
hole_offset_y = outer_width / 2 - hole_spacing / 2
result = (
    cq.Workplane("XY")
    .rect(outer_length, outer_width)
    .extrude(outer_height)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(hole_offset_x, hole_offset_y)
    .cutBlind(-hole_depth)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(hole_spacing, hole_spacing)
    .extrude(-hole_depth)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .rarray(hole_spacing, 0, hole_count, 1)
    .hole(hole_diameter)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .rarray(hole_spacing, 0, hole_count, 1)
    .hole(hole_diameter)
)
