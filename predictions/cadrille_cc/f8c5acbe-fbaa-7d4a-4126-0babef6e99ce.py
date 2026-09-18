import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
wall_thickness = 2.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset = 10.0
hole_offset = 15.0
hole_offset = 15.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg_length, 0)
    .lineTo(leg_length, thickness)
    .lineTo(leg_width, thickness)
    .lineTo(leg_width, leg_width)
    .lineTo(leg_width, leg_width)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(0, leg_length)
    .close()
    .extrude(thickness)
)
result = base.union(leg)
result = result.edges("|Z").chamfer(chamfer_size)
