import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
chamfer_size = 2.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 15.0
chamfer_distance = 1.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 15.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 15.0
base = (
    cq.Workplane("XY")
    .box(leg_length, leg_width, thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)
hole_positions = [
    (-hole_spacing_x/2, hole_spacing_y/2),
    (hole_spacing_x/2, hole_spacing_y/2),
    (-hole_spacing_x/2, hole_spacing_y/2),
    (hole_spacing_x/2, hole_spacing_y/2),
]
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
