import cadquery as cq
outer_width = 80.0
outer_height = 50.0
outer_height = 30.0
wall_thickness = 2.0
chamfer_distance = 0.5
hole_diameter = 5.0
hole_spacing = 12.0
hole_count = 6
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .rect(outer_width, outer_height)
    .extrude(outer_height)
)
base = base.edges("|Z").chamfer(chamfer_distance)
hole_positions = [
    (-hole_offset, -hole_spacing/2),
    (hole_offset, -hole_spacing/2),
    (-hole_offset, hole_spacing/2),
    (hole_offset, hole_spacing/2),
    (hole_offset, hole_spacing/2)
]
base = (
    base.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(outer_width - 2 * wall_thickness, outer_height - 2 * wall_thickness)
    .cutBlind(-wall_thickness)
)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(outer_width - 2 * wall_thickness, outer_height - wall_thickness)
    .cutBlind(-wall_thickness)
)
result = base
