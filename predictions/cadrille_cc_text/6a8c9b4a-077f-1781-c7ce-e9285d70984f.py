import cadquery as cq
outer_diameter = 80.0
pulley_thickness = 20.0
bearing_seat_radius = 15.0
bearing_seat_depth = 10.0
bearing_seat_radius = 30.0
bearing_seat_depth = 10.0
hole_diameter = 5.0
hole_pitch_radius = 30.0
hole_depth = 6.0
chamfer_size = 0.5
pocket_width = 12.0
pocket_height = 6.0
pocket_depth = 2.0
pocket_margin = 5.0
pocket_depth = 2.0
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - bearing_seat_radius
base = (
    cq.Workplane("XZ")
    .polyline([
        (outer_radius, 0),
        (outer_radius, pulley_thickness),
        (inner_radius, pulley_thickness),
        (inner_radius, pulley_thickness + bearing_seat_depth),
        (inner_radius, pulley_thickness + bearing_seat_depth),
        (inner_radius, pulley_thickness),
        (inner_radius, pulley_thickness),
        (inner_radius, 0),
        (inner_radius, 0)
    ])
    .close()
    .revolve()
)
pocket = (
    cq.Workplane("XY")
    .circle(pocket_width / 2.0)
    .extrude(pocket_depth)
)
pocket = pocket.cut(pocket)
pocket = (
    pocket.faces(">Z")
    .workplane()
    .circle(bearing_seat_radius)
    .extrude(bearing_seat_depth)
)
pocket = (
    pocket.faces(">Z")
    .workplane()
    .circle(pocket_width / 2.0)
    .extrude(pocket_depth)
)
result = pocket
