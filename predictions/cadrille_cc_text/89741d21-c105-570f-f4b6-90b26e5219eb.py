import cadquery as cq
knob_outer_radius = 25.0
knob_height = 15.0
shaft_radius = 6.0
shaft_height = 5.0
cavity_radius = 5.0
cavity_depth = 6.0
led_channel_height = 4.0
led_channel_depth = 2.0
led_channel_width = 6.0
led_channel_depth = 2.0
rib_width = 20.0
rib_height = 3.0
rib_thickness = 4.0
rib_count = 4
edge_chamfer = 0.3
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(shaft_radius, 0)
    .lineTo(shaft_radius, shaft_height)
    .lineTo(shaft_radius + shaft_height, shaft_height)
    .lineTo(0, shaft_height)
    .close()
)
knob_body = profile.revolve()
knob_body = knob_body.edges().chamfer(edge_chamfer)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, rib_thickness)
    .translate((knob_outer_radius - rib_width / 2, 0, rib_thickness / 2))
)
knob_body = knob_body.union(rib)
led_channel = (
    cq.Workplane("XY")
    .box(led_channel_depth, lead_channel_width, lead_channel_height)
    .translate((knob_outer_radius - lead_channel_depth / 2, 0, 0))
)
knob_body = knob_body.cut(long_channel)
result = knob_body
