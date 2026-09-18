import cadquery as cq

# Parameters
knob_outer_radius = 30.0
knob_base_height = 12.0
knob_step_radius = 22.0
knob_step_height = 8.0
shaft_radius = 8.0
shaft_length = 20.0
ring_thickness = 5.0
ring_height = 6.0
ring_gap_width = 4.0
chamfer_distance = 1.2

# Base knob body with stepped profile
base_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(knob_outer_radius, 0)
    .lineTo(knob_outer_radius, knob_base_height)
    .lineTo(knob_step_radius, knob_base_height)
    .lineTo(knob_step_radius, knob_base_height + knob_step_height)
    .lineTo(0, knob_base_height + knob_step_height)
    .close()
)

knob_body = base_profile.revolve()

# Central shaft hole
knob_with_hole = (
    knob_body
    .faces(">Z")
    .workplane()
    .hole(shaft_radius * 2)
)

# Split ring creation
ring_profile = (
    cq.Workplane("XY")
    .moveTo(knob_outer_radius, 0)
    .lineTo(knob_outer_radius + ring_thickness, 0)
    .lineTo(knob_outer_radius + ring_thickness, ring_height)
    .lineTo(knob_outer_radius, ring_height)
    .close()
)

ring = ring_profile.revolve()

# Gap cut for split ring
gap_cut = (
    cq.Workplane("XY")
    .box(ring_gap_width, ring_height * 2, ring_height * 2)
    .translate((knob_outer_radius + ring_thickness / 2, 0, ring_height / 2))
)

ring_split = ring.cut(gap_cut)

# Assemble knob and split ring
assembled = knob_with_hole.union(ring_split)

# Chamfer top edge of knob
result = assembled.faces(">Z").edges().chamfer(chamfer_distance)
