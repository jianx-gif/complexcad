import cadquery as cq

# Parameters
leg_length = 80.0
leg_width = 40.0
thickness = 10.0
fillet_radius = 2.0
hole_diameter = 4.0
hole_spacing = 15.0
hole_count = 4
hole_offset = 12.0
notch_radius = 4.0

# L‑profile sketch with a circular notch on the horizontal leg
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg_width, 0)
    .lineTo(leg_width, thickness)
    .lineTo(thickness, thickness)
    .lineTo(thickness, leg_length)
    .lineTo(0, leg_length)
    .close()
    .moveTo(leg_width / 2, thickness / 2)
    .circle(notch_radius)
)

# Extrude to create solid
solid = profile.extrude(thickness)

# Fillet inner corner (vertical edge at origin)
solid = solid.edges("|Z and <X and <Y").fillet(fillet_radius)

# Drill clearance holes on the vertical leg (top face)
result = (
    solid.faces(">Z")
    .workplane()
    .moveTo(thickness / 2, hole_offset)
    .rarray(0, hole_spacing, 1, hole_count)
    .hole(hole_diameter)
)
