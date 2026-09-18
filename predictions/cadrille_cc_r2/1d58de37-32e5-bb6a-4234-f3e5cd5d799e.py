import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
chamfer_size = 2.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 15.0
chamfer_distance = 1.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 15.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 15.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 15.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 15.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = hole_spacing_x / 2
hole_spacing_y = hole_spacing_y / 2
hole_points = [
    (hole_cols - 1) * hole_spacing_x, hole_spacing_y / 2),
    (leg_length, 0),
    (leg_length, leg_width),
    (leg_width, leg_width),
    (leg_width, leg_width + thickness),
    (leg_width, leg_width + thickness + thickness),
    (leg_width, leg_width + thickness + thickness + leg_width),
    (leg_width, leg_width + thickness + leg_width),
    (leg_width, leg_width + leg_width + leg_width),
    (leg_width, leg_width + leg_width + leg_width),
    (leg_width, leg_width + leg_width + leg_width)
]
result = (
    cq.Workplane("XY")
    .polyline(hole_points)
    .close()
    .extrude(thickness)
)
result = result.edges("|Z").chamfer(chamfer_distance)
result = result.edges("|X").chamfer(chamfer_distance)
