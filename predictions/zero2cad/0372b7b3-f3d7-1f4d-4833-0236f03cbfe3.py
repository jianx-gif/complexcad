import cadquery as cq

# Parameters
knob_outer_radius = 20.0
knob_height = 30.0
shaft_radius = 6.0
shaft_length = 12.0
wall_thickness = 2.0
fillet_radius = 1.0
slot_width = 4.0
slot_depth = 6.0
slot_height = 10.0

# Base knob profile (XZ plane) and revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(knob_outer_radius, 0)
    .lineTo(knob_outer_radius, knob_height - 8)
    .threePointArc((knob_outer_radius - 4, knob_height - 4), (knob_outer_radius - 8, knob_height))
    .lineTo(0, knob_height)
    .close()
)

knob_body = profile.revolve()

# Add central shaft
knob_with_shaft = (
    knob_body
    .faces("<Z")
    .workplane()
    .circle(shaft_radius)
    .extrude(shaft_length)
)

# Fillet transition between shaft and knob body
knob_fillet = knob_with_shaft.edges().fillet(fillet_radius)

# Create side slot for cable routing
slot = (
    cq.Workplane("XY")
    .center(knob_outer_radius - wall_thickness/2, knob_height/2)
    .rect(slot_width, slot_height)
    .extrude(-slot_depth)
)

result = knob_fillet.cut(slot)
