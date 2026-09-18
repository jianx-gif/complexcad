import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
wall_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset = 10.0
hole_offset = 15.0
hole_offset = 15.0
hole_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .box(leg_length, leg_width, thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)
hole_positions = [
    (hole_offset, 0),
    (leg_length, 0),
    (leg_length, leg_width),
    (leg_width, leg_width),
    (leg_width, leg_width),
    (0, leg_width),
]
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(hole_offset, hole_offset)
    .hole(hole_diameter)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(hole_offset, hole_offset)
    .hole(hole_diameter)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(hole_offset, hole_offset)
    .hole(hole_diameter)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(hole_offset, hole_offset)
    .hole(hole_diameter)
)
