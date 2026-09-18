import cadquery as cq

# Parameters
inner_radius = 15.0
wall_thickness = 5.0
outer_radius = inner_radius + wall_thickness
clip_length = 60.0
bend_radius = 10.0
knurl_cylinder_dia = 2.0
knurl_depth = 0.8
knurl_cols = 12
relief_hole_dia = 8.0
relief_hole_offset = 30.0
chamfer_distance = 1.0

# Main clip: profile revolved around Z
clip = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, clip_length - bend_radius)
    .threePointArc((inner_radius + bend_radius, clip_length), (outer_radius, clip_length))
    .lineTo(outer_radius, 0)
    .close()
    .revolve()
    .tag("clip_body")
)

# Chamfer bottom edges
clip = (
    clip
    .faces("<Z")
    .edges()
    .chamfer(chamfer_distance)
)

# Relief hole through body at specified offset
clip = (
    clip
    .workplaneFromTagged("clip_body")
    .center(0, relief_hole_offset)
    .circle(relief_hole_dia / 2)
    .cutThruAll()
)

# Knurled grip: shallow cylindrical cuts on outer cylindrical face
circum_spacing = 2 * 3.1415926535 * outer_radius / knurl_cols
clip = (
    clip
    .faces("|Z")
    .workplane()
    .rarray(circum_spacing, 0, knurl_cols, 1)
    .circle(knurl_cylinder_dia / 2)
    .cutBlind(-knurl_depth)
)

result = clip