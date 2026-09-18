import cadquery as cq

# Parameters
clip_length = 60.0
clip_thickness = 5.0
inner_radius = 15.0
outer_radius = inner_radius + clip_thickness
tip_radius = 8.0
hole_diameter = 8.0
knurl_width = 2.0
knurl_depth = 1.0
knurl_count = 12

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, clip_length - tip_radius)
    .threePointArc((outer_radius + tip_radius, clip_length - tip_radius), (outer_radius, clip_length))
    .lineTo(outer_radius, 0)
    .close()
)

# Revolve to create clip body
clip_body = profile.revolve()

# Central through hole (cylinder along Y axis)
hole_cylinder = (
    cq.Workplane("XZ")
    .center(0, clip_length / 2)
    .circle(hole_diameter / 2)
    .extrude(clip_length * 2)
)
clip_body = clip_body.cut(hole_cylinder)

# Knurl pattern: radial cuts around outer surface
knurl_cuts = (
    cq.Workplane("XZ")
    .polarArray(radius=outer_radius - knurl_depth / 2, startAngle=0, angle=360, count=knurl_count)
    .rect(knurl_width, knurl_depth)
    .extrude(clip_length)
)
clip_body = clip_body.cut(knurl_cuts)

result = clip_body