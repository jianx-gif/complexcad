import cadquery as cq

clamp_body_length = 60
jaw_length = 20
total_diameter = 30
outer_radius = total_diameter / 2
wall_thickness = 4
inner_radius = outer_radius - wall_thickness
jaw_extension = 8
chamfer = 1.5
internal_fillet_radius = 2
set_screw_hole_dia = 4
set_screw_count = 4
set_screw_spacing = 10
set_screw_start = 12

profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (outer_radius, 0),
        (outer_radius, clamp_body_length - jaw_length),
        (outer_radius + jaw_extension, clamp_body_length),
        (0, clamp_body_length),
    ])
    .close()
)

body = profile.revolve()

# internal fillet via subtractive cylinder at inner bottom corner
fillet_cut = (
    cq.Workplane("XZ")
    .center(inner_radius, 0)
    .circle(internal_fillet_radius)
    .extrude(internal_fillet_radius * 2)
)
body = body.cut(fillet_cut)

# chamfer on outer top edge
body = body.faces(">Z").edges().chamfer(chamfer)

# set screw holes pattern along inner wall
for i in range(set_screw_count):
    z = set_screw_start + i * set_screw_spacing
    hole = (
        cq.Workplane("XZ")
        .center(inner_radius + wall_thickness / 2, z)
        .circle(set_screw_hole_dia / 2)
        .extrude(wall_thickness + 2)
    )
    body = body.cut(hole)

result = body