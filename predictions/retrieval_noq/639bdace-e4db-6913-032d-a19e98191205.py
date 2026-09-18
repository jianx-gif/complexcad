import cadquery as cq

# Parameters
outer_radius_collar = 30.0
inner_radius_collar = 20.0
flange_outer_radius = 45.0
collar_length = 30.0
shoulder_length = 10.0
flange_thickness = 8.0
wall_thickness = outer_radius_collar - inner_radius_collar
chamfer_size = 0.5
hole_diameter = 5.0
counterbore_diameter = 10.0
counterbore_depth = 4.0
hole_pattern_radius = 25.0
pocket_depth = 4.0
pocket_radius = 12.0

pts = [
    (outer_radius_collar, 0),
    (outer_radius_collar, collar_length),
    (outer_radius_collar, collar_length + shoulder_length),
    (flange_outer_radius, collar_length + shoulder_length),
    (flange_outer_radius, collar_length + shoulder_length + flange_thickness),
    (0, collar_length + shoulder_length + flange_thickness),
    (0, 0),
]

solid_body = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .revolve()
)

hollow_body = solid_body.shell(wall_thickness)

flange_holes = (
    hollow_body
    .faces("+Z")
    .workplane()
    .pushPoints([
        (hole_pattern_radius, 0),
        (-hole_pattern_radius/2, hole_pattern_radius*0.86602540378),
        (-hole_pattern_radius/2, -hole_pattern_radius*0.86602540378),
        (0, -hole_pattern_radius),
    ])
    .hole(hole_diameter)
    .hole(counterbore_diameter, depth=counterbore_depth)
)

pocket = (
    flange_holes
    .faces("-Z")
    .workplane()
    .center(0, 0)
    .hole(pocket_radius, depth=pocket_depth)
)

result = (
    pocket
    .edges("#Z")
    .chamfer(chamfer_size)
)
