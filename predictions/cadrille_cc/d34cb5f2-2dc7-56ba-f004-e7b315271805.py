import cadquery as cq
leg_length = 80.0
leg_width = 20.0
thickness = 10.0
wall_thickness = 2.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset = 10.0
hole_offset = 15.0
hole_offset_y = 0.0
hole_spacing = 30.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 20.0
hole_offset_y = 0.0
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg_length, 0)
    .lineTo(leg_length, thickness)
    .lineTo(leg_width, thickness)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length + hole_offset_y)
    .lineTo(hole_offset, leg_length + hole_offset_y)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .lineTo(hole_offset, leg_length)
    .close()
)
result = base
