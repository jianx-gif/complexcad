import cadquery as cq
horizontal_length = 70.0
vertical_length = horizontal_length
leg_thickness = 12.0
bracket_depth = 10.0
rib_width = 6.0
rib_height = 8.0
rib_depth = 4.0
rib_spacing = 15.0
hole_diameter = 5.0
hole_spacing_x = 20.0
hole_spacing_y = 25.0
hole_rows = 2
hole_cols = 3
hole_spacing_y = 25.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (horizontal_length, 0),
        (horizontal_length, vertical_length),
        (leg_thickness, vertical_length),
        (leg_thickness, leg_thickness),
        (0, leg_thickness),
        (0, 0)
    ])
    .close()
    .extrude(bracket_depth)
)
rib = (
    base.faces(">Z")
    .workplane()
    .center(leg_thickness/2, vertical_length/2)
    .rect(rib_width, rib_height)
    .extrude(rib_depth)
)
bracket = (
    rib.faces(">Z")
    .workplane()
    .center(leg_thickness/2, vertical_length/2)
    .rarray(hole_spacing_x, hole_spacing_y, hole_cols, hole_rows)
    .hole(hole_diameter)
)
bracket = (
    bracket.faces(">Z")
    .workplane()
    .center(leg_thickness/2, vertical_length/2)
    .rarray(hole_spacing_x, hole_spacing_y, hole_cols, hole_rows)
    .hole(hole_diameter)
)
result = bracket
