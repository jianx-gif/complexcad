import cadquery as cq
outer_diameter = 50.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = inner_diameter / 2.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 12
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .rect(outer_diameter, outer_diameter)
    .extrude(outer_diameter)
)
base = base.edges().chamfer(chamfer_size)
hole_positions = [
    (inner_diameter / 2.0, inner_diameter / 2.0),
    (-inner_diameter / 2.0, inner_diameter / 2.0),
    ( inner_diameter / 2.0, inner_diameter / 2.0),
    (-inner_diameter / 2.0, inner_diameter / 2.0),
    ( inner_diameter / 2.0, inner_diameter / 2.0),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .rect(inner_diameter, inner_diameter)
    .cutBlind(-inner_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .rect(inner_diameter - 2 * wall_thickness, inner_diameter - 2 * wall_thickness)
    .cutBlind(-wall_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .rect(inner_diameter - 2 * wall_thickness, inner_diameter - 2 * wall_thickness)
    .cutBlind(-wall_thickness)
)
result = base
