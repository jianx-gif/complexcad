import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
wall_thickness = 2.0
chamfer_distance = 1.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 4
hole_offset = 10.0
chamfer_distance = 0.5
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg_length, 0)
    .lineTo(leg_length, leg_width)
    .lineTo(leg_width, leg_width)
    .lineTo(leg_width, leg_width)
    .lineTo(leg_width, leg_length)
    .lineTo(0, leg_length)
    .close()
    .extrude(thickness)
)
base = base.edges("|Z").chamfer(chamfer_distance)
hole_positions = [
    (hole_offset, hole_offset),
    (hole_offset, hole_offset),
    (hole_offset, hole_offset),
    (hole_offset, hole_offset),
]
base = base.faces(">Z").workplane().pushPoints(hole_positions).hole(hole_diameter)
base = base.faces(">Z").edges().chamfer(chamfer_distance)
result = base
