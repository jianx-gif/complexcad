import cadquery as cq

# Parameters
outer_radius = 30.0
hub_radius = 12.0
hub_height = 15.0
shoulder_height = 5.0
knob_height = 20.0
shaft_radius = 4.0
set_screw_radius = 2.5
set_screw_offset = 15.0
chamfer_size = 1.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(hub_radius, 0)
    .lineTo(hub_radius, hub_height)
    .lineTo(outer_radius, hub_height + shoulder_height)
    .lineTo(outer_radius, hub_height + shoulder_height + knob_height)
    .lineTo(0, hub_height + shoulder_height + knob_height)
    .close()
)

# Revolve to create knob body
knob_body = profile.revolve()

# Central shaft hole (through all)
shaft_hole = (
    cq.Workplane("XY")
    .circle(shaft_radius)
    .extrude(hub_height + shoulder_height + knob_height + 2)
)

# Set screw clearance hole (offset from center)
set_screw_hole = (
    cq.Workplane("XY")
    .center(set_screw_offset, 0)
    .circle(set_screw_radius)
    .extrude(hub_height + shoulder_height + knob_height + 2)
)

# Combine features
result = (
    knob_body
    .cut(shaft_hole)
    .cut(set_screw_hole)
    .edges("|Z")
    .chamfer(chamfer_size)
)
