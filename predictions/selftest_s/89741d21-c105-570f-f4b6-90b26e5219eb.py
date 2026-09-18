import cadquery as cq

# Parameters
knob_outer_radius = 25.0
knob_height = 15.0
shaft_radius = 6.0
shaft_height = 5.0
cavity_radius = 5.0
cavity_depth = 6.0
cavity_fillet = 0.1
led_channel_width = 6.0
led_channel_height = 4.0
led_channel_depth = 2.0
led_channel_offset_z = knob_height - led_channel_height - 2.0
rib_width = 20.0
rib_thickness = 4.0
rib_height = 3.0
rib_inset = 0.5
edge_chamfer = 0.3

# Base knob profile (revolve)
base_profile = (
    cq.Workplane("XY")
    .moveTo(shaft_radius, 0)
    .lineTo(shaft_radius, shaft_height)
    .threePointArc((knob_outer_radius, shaft_height + 2), (knob_outer_radius, knob_height))
    .lineTo(0, knob_height)
    .close()
)

result = base_profile.revolve()

# Central light diffusion cavity cut
cavity = cq.Workplane("XY").circle(cavity_radius).extrude(-cavity_depth)
result = result.cut(cavity)

# LED recessed channel (rectangular cut)
led_cut = (
    cq.Workplane("XY")
    .center(knob_outer_radius - led_channel_depth / 2, led_channel_offset_z)
    .box(led_channel_depth, led_channel_width, led_channel_height)
)
result = result.cut(led_cut)

# Fillet interior edge of cavity (perpendicular to Z)
result = result.edges("#Z").fillet(cavity_fillet)

# Bottom mounting rib (integrated with body)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_thickness, rib_height)
    .translate((0, 0, -rib_height/2 + rib_inset))
)
result = result.union(rib)

# Chamfer outer top rim edge (farthest in +Z)
result = result.edges(">>Z").chamfer(edge_chamfer)
