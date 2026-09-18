import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
chamfer_size = 2.0
hole_diameter = 5.0
hole_spacing = 15.0
hole_offset = 12.0
chamfer_distance = 1.0
hole_count = 6
hole_count = 6
hole_radius = hole_diameter / 2.0
hole_offset = hole_offset + thickness / 2.0
base = (
    cq.Workplane("XY")
    .rect(leg_length, leg_width)
    .extrude(thickness)
)
base = base.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, -hole_offset),
    (hole_offset, hole_offset),
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
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(hole_offset, hole_offset)
    .hole(hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(hole_offset, hole_offset)
    .hole(hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(hole_offset, hole_offset)
    .hole(hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(hole_offset, hole_offset)
    .hole(hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(hole_offset, hole_offset)
    .hole(hole_diameter)
)
result = base
