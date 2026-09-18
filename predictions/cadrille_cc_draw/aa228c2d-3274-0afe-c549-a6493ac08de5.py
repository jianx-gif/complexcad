import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 8.0
wall_thickness = 2.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset = 10.0
chamfer_size = 0.5
hole_spacing = 20.0
hole_count = 3
hole_offset = 15.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_width, 0),
        (leg_width, thickness),
        (thickness, thickness),
        (thickness, leg_length),
        (0, leg_length),
        (0, 0)
    ])
    .close()
    .extrude(thickness)
)
hole_positions = [
    (hole_offset, leg_length / 2),
    (leg_width / 2, leg_length / 2),
    (thickness / 2, leg_length / 2),
    (thickness / 2, leg_length / 2)
]
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
