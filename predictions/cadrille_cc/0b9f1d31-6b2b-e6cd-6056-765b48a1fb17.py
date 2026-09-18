import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 5.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset = 10.0
hole_offset_y = 0.0
hole_spacing = 30.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 20.0
hole_offset_y = 0.0
base = (
    cq.Workplane("XY")
    .box(leg_length, leg_width, thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(leg_length/2, hole_offset_y)
    .rect(hole_spacing, hole_offset_y)
    .cutBlind(-thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(leg_length/2, hole_offset_y)
    .hole(hole_diameter)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(leg_length/2, hole_offset_y)
    .hole(hole_diameter)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(leg_length/2, hole_offset_y)
    .hole(hole_diameter)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(leg_length/2, hole_offset_y)
    .hole(hole_diameter)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(leg_length/2, hole_offset_y)
    .hole(hole_diameter)
)
result = base
