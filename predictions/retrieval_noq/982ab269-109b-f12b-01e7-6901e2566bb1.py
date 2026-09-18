import cadquery as cq

# Dimensions (max 100 units scale)
knob_total_height = 20.0
base_radius = 10.0
outer_radius = 15.0
groove_height = 5.0
groove_depth = 1.5
groove_radius = outer_radius - 2.0
hex_flat_to_flat = 6.0
hex_height = 4.0
fillet_radius = 0.8

# Sketch profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, knob_total_height - groove_height)
    .lineTo(outer_radius, knob_total_height - groove_height)
    .lineTo(outer_radius, knob_total_height)
    .lineTo(0, knob_total_height)
    .close()
)

# Revolve main knob body
base_body = profile.revolve()

# Add central hexagonal boss (fused)
body_with_hex = (
    base_body.faces(">Z").workplane()
    .polygon(6, hex_flat_to_flat)
    .extrude(hex_height)
)

# Cut peripheral groove near the top
knob = (
    body_with_hex.faces(">Z").workplane()
    .circle(groove_radius)
    .cutBlind(-groove_depth)
)

# Apply fillet to vertical edges for safety
result = knob.edges("|Z").fillet(fillet_radius)
