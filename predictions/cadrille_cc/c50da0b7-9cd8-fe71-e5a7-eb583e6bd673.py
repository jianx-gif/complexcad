import cadquery as cq
leg_length = 80.0
leg_width = 20.0
thickness = 10.0
wall_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 4
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 12.0
hole_spacing_y = 12.0
hole_spacing_y = 15.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(leg_length, leg_width)
    .extrude(thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(leg_width/2, leg_width/2)
    .rect(hole_spacing_x, hole_spacing_y)
    .cutBlind(-thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(leg_width/2, leg_width/2)
    .rect(hole_spacing_x, hole_spacing_y)
    .cutBlind(-thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(leg_width/2, hole_spacing_y)
    .hole(hole_diameter)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(leg_width/2, hole_spacing_y)
    .hole(hole_diameter)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(leg_width/2, hole_spacing_y)
    .hole(hole_diameter)
)
result = base
