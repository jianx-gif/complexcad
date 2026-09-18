import cadquery as cq
hex_outer_diameter = 80.0
hex_outer_radius = hex_outer_diameter / 2.0
total_height = 80.0
circle_radius = hex_outer_diameter / 2.0
circle_radius = hex_outer_radius - radius_radius
circle_radius = hex_outer_radius - radius_radius
circle_radius = hex_radius - radius_radius
circle_radius = hex_radius - radius_radius
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(0, total_height)
    .lineTo(0, total_height)
    .lineTo(0, 0)
    .close()
)
result = profile.extrude(total_height)
