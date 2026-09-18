import cadquery as cq
leg_length = 80.0
leg_width = 20.0
thickness = 10.0
wall_thickness = 2.0
chamfer_distance = 0.5
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_width, 0),
        (leg_width, thickness),
        (leg_width, leg_length),
        (0, leg_length),
        (0, 0)
    ])
    .close()
    .extrude(thickness)
)
hole_positions = [
    (-hole_spacing / 2, 0),
    (hole_spacing / 2, 0)
]
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
