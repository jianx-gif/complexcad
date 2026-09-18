import cadquery as cq

# Dimensions
knob_base_radius = 20.0
knob_base_height = 8.0
knob_shoulder_radius = 15.0
knob_shoulder_height = 6.0
clearance_bore_radius = 5.0
ring_inner_radius = 22.0
ring_outer_radius = 25.0
ring_height = 4.0
split_gap_width = 3.0
chamfer_distance = 0.8

# Base knob body with shoulder and central bore
knob_body = (
    cq.Workplane("XY")
    .circle(knob_base_radius)
    .extrude(knob_base_height)
    .faces(">Z")
    .workplane()
    .tag("knob_body")
    .workplaneFromTagged("knob_body")
    .circle(knob_shoulder_radius)
    .extrude(knob_shoulder_height)
    .faces(">Z")
    .workplane()
    .hole(clearance_bore_radius * 2)
)
# Chamfer top outer rim edge (horizontal) of knob body
knob_body = knob_body.edges(">Z").chamfer(chamfer_distance)

# Split ring collar profile and revolve
ring_profile = (
    cq.Workplane("XY")
    .moveTo(ring_inner_radius, 0)
    .lineTo(ring_inner_radius, ring_height)
    .lineTo(ring_outer_radius, ring_height)
    .lineTo(ring_outer_radius, 0)
    .close()
)
ring = ring_profile.revolve()
# Split gap cut through the ring
split_cut = (
    cq.Workplane("XY")
    .box(split_gap_width, ring_outer_radius * 2, ring_height * 2)
    .translate(((ring_inner_radius + ring_outer_radius) / 2, 0, 0))
)
ring = ring.cut(split_cut)
# Position ring on top of shoulder
ring = ring.translate((0, 0, knob_base_height + knob_shoulder_height))
# Combine knob body and ring collar
result = knob_body.union(ring)
