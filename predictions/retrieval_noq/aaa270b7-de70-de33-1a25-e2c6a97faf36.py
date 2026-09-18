import cadquery as cq

impeller_outer_radius = 40.0
hub_height = 20.0
chute_extension = 15.0
chute_height = 30.0
wall_thickness = 2.0
channel_radius = 1.5
channel_pitch = 8.0
channel_turns = 4
channel_length = channel_pitch * channel_turns
chamfer_dist = 0.5
shaft_bore_radius = 4.0

impeller_body = (
    cq.Workplane('XY')
    .circle(impeller_outer_radius)
    .workplane(offset=hub_height)
    .circle(impeller_outer_radius)
    .workplane(offset=chute_height)
    .circle(impeller_outer_radius + chute_extension)
    .loft()
)

helix = cq.Wire.makeHelix(pitch=channel_pitch, radius=impeller_outer_radius - wall_thickness - channel_radius, height=channel_length)
helix = helix.translate((0, 0, hub_height / 2))
spiral_profile = cq.Workplane('XY').circle(channel_radius)
spiral_cut = spiral_profile.sweep(helix)

impeller_with_channel = impeller_body.cut(spiral_cut)

shaft_bore = cq.Workplane('XY').circle(shaft_bore_radius).extrude(hub_height + chute_height)
impeller_with_bore = impeller_with_channel.cut(shaft_bore)

result = impeller_with_bore.faces('>Z').edges().chamfer(chamfer_dist)
