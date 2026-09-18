import cadquery as cq

# Parameters
base_radius = 30.0
base_height = 5.0
frame_width = 60.0
frame_depth = 40.0
frame_height = 8.0
hole_diameter = 3.0
hole_spacing_x = 20.0
hole_spacing_y = 15.0
chamfer_size = 0.5

# Base created by revolving a rectangular profile
base = (
    cq.Workplane("XZ")
    .moveTo(base_radius, 0)
    .lineTo(base_radius, base_height)
    .lineTo(0, base_height)
    .close()
    .revolve()
)

# Raised rectangular frame on top of the base
frame = (
    base
    .faces(">Z")
    .workplane()
    .rect(frame_width, frame_depth)
    .extrude(frame_height)
)

# Chamfer vertical edges of the raised frame
frame = (
    frame
    .edges("|Z")
    .chamfer(chamfer_size)
)

# Add four screw holes in a rectangular pattern on the top face of the frame
result = (
    frame
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-hole_spacing_x/2, -hole_spacing_y/2),
        (hole_spacing_x/2, -hole_spacing_y/2),
        (-hole_spacing_x/2, hole_spacing_y/2),
        (hole_spacing_x/2, hole_spacing_y/2),
    ])
    .hole(hole_diameter)
    .edges("<<Z")
    .chamfer(chamfer_size)
)
