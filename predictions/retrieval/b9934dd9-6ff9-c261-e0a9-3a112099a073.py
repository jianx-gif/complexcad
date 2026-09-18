import cadquery as cq

# Parameters
body_outer_radius = 25.0
body_inner_radius = 15.0
body_height = 40.0
shoulder_height = 5.0
base_thickness = 5.0
base_radius = body_outer_radius + 5.0
blind_hole_dia = 3.0
blind_hole_depth = 8.0
num_blind_holes = 8
mounting_hole_dia = 6.0
mounting_hole_spacing = 30.0
chamfer_size = 1.0

# Base flange
flange = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(base_thickness)
)

# Mounting holes on flange (four-hole rectangular pattern)
flange = (
    flange.faces(">Z")
    .workplane()
    .rarray(mounting_hole_spacing, mounting_hole_spacing, 2, 2)
    .hole(mounting_hole_dia)
)

# Valve body profile with built-in chamfer
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius - chamfer_size, 0)
    .lineTo(base_radius, chamfer_size)
    .vLine(base_thickness - chamfer_size)
    .lineTo(body_outer_radius, base_thickness + shoulder_height - chamfer_size)
    .lineTo(body_outer_radius + chamfer_size, base_thickness + shoulder_height)
    .vLine(body_height - (base_thickness + shoulder_height))
    .lineTo(body_inner_radius, body_height)
    .vLine(-(body_height - (base_thickness + shoulder_height)))
    .close()
)

# Revolve profile around Z axis to form body
body = profile.revolve()

# Union body with flange
assembly = flange.union(body)

# Radial blind holes on the outer cylindrical surface
hole_plane = cq.Workplane("XY").transformed(offset=(0, 0, base_thickness + shoulder_height / 2))
blind_hole = (
    hole_plane.polarArray(radius=body_outer_radius - 2.0, count=num_blind_holes, startAngle=0, angle=360)
    .circle(blind_hole_dia / 2)
    .extrude(blind_hole_depth)
)
assembly = assembly.cut(blind_hole)

result = assembly