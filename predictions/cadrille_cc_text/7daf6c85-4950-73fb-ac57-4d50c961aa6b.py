import cadquery as cq
leg_length_long = 80.0
leg_length_short = 60.0
bracket_thickness = 8.0
inner_fillet_radius = 2.0
clearance_hole_diameter = 4.0
hole_offset_x = 30.0
hex_radius = 6.0
hex_radius = hex_radius + 2.0
hex_width = 20.0
hex_thickness = bracket_thickness
profile = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_length_long, 0),
        (leg_length_long, leg_width),
        (leg_width, leg_width),
        (leg_width, leg_length_short),
        (leg_length_long, leg_length_short),
        (leg_length_long, leg_width),
        (0, leg_width),
        (0, 0)
    ])
    .close()
)
result = profile.extrude(bracket_thickness)
result = result.edges("|Z").fillet(inner_fillet_radius)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, leg_width/2)
    .polygon(6, hex_radius)
    .cutBlind(-hex_thickness)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, leg_width/2)
    .polygon(6, hex_radius)
    .cutBlind(-hex_thickness)
)
