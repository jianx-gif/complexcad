import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
height = 20.0
wall_thickness = 2.0
chamfer_distance = 0.5
hole_diameter = 5.0
hole_spacing = 30.0
hole_count = 6
hole_count = 6
hole_radius = outer_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
)
inner = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(height)
)
base = base.cut(inner)
hole_positions = [
    (hole_count, 0),
    (-hole_count, 0),
    (0, hole_radius),
    (0, -hole_radius),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
base = base.edges("|Z").chamfer(chamfer_distance)
result = base
