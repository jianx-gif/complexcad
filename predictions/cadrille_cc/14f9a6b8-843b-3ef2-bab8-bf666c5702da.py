import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
wall_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_offset = 10.0
hole_offset = 15.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 12.0
hole_spacing_y = 15.0
hole_spacing_y = 15.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = hole_offset + hole_spacing_x
hole_spacing_y = hole_spacing_y
hole_spacing_y = hole_spacing_y
hole_rows = [(hole_spacing_x + i * hole_spacing_x, hole_spacing_y) for i in range(hole_cols)]
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg_width, 0)
    .lineTo(leg_width, leg_width)
    .lineTo(leg_width, leg_width)
    .lineTo(leg_width, leg_width)
    .lineTo(leg_width, leg_width)
    .lineTo(leg_width, leg_width)
    .lineTo(leg_width, leg_width)
    .lineTo(leg_width, leg_width)
    .lineTo(leg_width, leg_width)
    .lineTo(leg_width, leg_width)
    .lineTo(leg_width, leg_width)
    .lineTo(hole_spacing_x, leg_width)
    .lineTo(hole_spacing_y, leg_width)
    .close()
    .extrude(thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)
