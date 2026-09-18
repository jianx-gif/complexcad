import cadquery as cq
from math import pi

# Parameters (max dimension 100)
outer_diameter = 60.0
inner_diameter = 20.0
spacer_height = 30.0
central_hole_diameter = 10.0
groove_width = 3.0
groove_depth = 2.0
helix_pitch = 5.0
fillet_radius = 1.0
notch_width = 5.0

# Composite profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2, 0)
    .lineTo(inner_diameter / 2, spacer_height)
    .lineTo(outer_diameter / 2, spacer_height)
    .lineTo(outer_diameter / 2, spacer_height / 2)
    .lineTo(outer_diameter / 2 - notch_width, spacer_height / 2)
    .lineTo(outer_diameter / 2 - notch_width, 0)
    .lineTo(inner_diameter / 2, 0)
    .close()
)

solid = profile.revolve(360)

# Fillet on inner cylindrical surface (acts on inner wall edges)
solid = solid.fillet(fillet_radius)

# Central through hole
solid = solid.faces("<Z").workplane().hole(central_hole_diameter)

# Helical groove path (Wire)
helix = cq.Wire.makeHelix(pitch=helix_pitch, height=spacer_height, radius=(outer_diameter/2 - groove_depth/2))

# Groove cross‑section (XZ plane) – rectangular slot
groove_profile = (
    cq.Workplane("XZ")
    .moveTo(groove_width/2, 0)
    .lineTo(groove_width/2, groove_depth)
    .lineTo(-groove_width/2, groove_depth)
    .lineTo(-groove_width/2, 0)
    .close()
)

groove = groove_profile.sweep(helix)

result = solid.cut(groove)
