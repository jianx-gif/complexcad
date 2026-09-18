import cadquery as cq
outer_radius = 25.0
inner_radius = 20.0
cap_height = 30.0
grip_ring_height = 8.0
knurl_width = 2.0
knurl_height = 3.0
knurl_depth = 12.0
pilot_diameter = 5.0
pilot_depth = 12.0
pilot_radius = outer_radius - inner_radius
chamfer_size = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, cap_height - grip_ring_height)
    .lineTo(inner_radius, cap_height - grip_ring_height)
    .lineTo(inner_radius, 0)
    .close()
)
knurl = profile.revolve()
knurl = (
    cq.Workplane("XY")
    .box(knurl_depth, knurl_width, knurl_height)
    .translate((outer_radius - knurl_depth/2, 0, 0))
)
knurl = knurl.union(knurl)
knurl = (
    cq.Workplane("XY")
    .box(knurl_depth, knurl_width, knurl_height)
    .translate((outer_radius - knurl_depth/2, 0, 0))
)
knurl = (
    cq.Workplane("XY")
    .box(knurl_depth, knurl_width, knurl_height)
    .translate((outer_radius - knurl_depth/2, 0, 0))
)
knurl = (
    cq.Workplane("XY")
    .box(knurl_depth, knurl_width, knurl_height)
    .translate((outer_radius - knurl_depth/2, 0, 0))
)
knurl = knurl.union(knurl)
result = knob.edges().chamfer(chamfer_size)
