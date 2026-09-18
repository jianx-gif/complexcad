import cadquery as cq

# Parameters
leg_length = 60.0
leg_width = 30.0
thickness = 8.0
chamfer_size = 0.8
hole_diameter = 4.0
hole_depth = 12.0
hole_spacing = 15.0
hole_count = 3
hole_start_offset = 10.0

# L‑profile points (XY plane)
profile_pts = [
    (thickness, 0),
    (thickness, leg_length),
    (thickness + leg_width, leg_length),
    (thickness + leg_width, leg_length - thickness),
    (thickness, leg_length - thickness),
    (thickness, 0),
]

# Revolve profile to create bracket
result = (
    cq.Workplane("XY")
    .polyline(profile_pts)
    .close()
    .revolve(360)
)

# Chamfer all edges for safety
result = result.edges().chamfer(chamfer_size)

# Blind holes on inner cylindrical face (radial direction)
inner_face = result.faces("|Z")
for i in range(hole_count):
    y_pos = hole_start_offset + i * hole_spacing
    result = (
        inner_face.workplane()
        .center(0, y_pos)
        .circle(hole_diameter / 2)
        .cutBlind(-hole_depth)
    )
