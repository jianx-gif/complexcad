import cadquery as cq

# Parameters
knob_outer_radius = 30.0
knob_height = 20.0
base_radius = 15.0
base_height = 5.0
central_hole_diameter = 8.0
chamfer_distance = 1.5
slot_width = 8.0
slot_length = 15.0
slot_depth = 10.0

# Create 2D profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, base_height)
    .lineTo(base_radius, base_height)
    .threePointArc((knob_outer_radius, base_height + knob_height / 2), (knob_outer_radius, base_height + knob_height))
    .lineTo(0, base_height + knob_height)
    .close()
)

# Revolve profile around Z axis to form knob body
knob_body = profile.revolve()

# Central through hole
knob_with_hole = knob_body.faces(">Z").workplane().hole(central_hole_diameter)

# Chamfer outer edges
knob_chamfered = knob_with_hole.edges().chamfer(chamfer_distance)

# Slot cut on top face
result = (
    knob_chamfered
    .faces(">Z")
    .workplane()
    .rect(slot_length, slot_width)
    .cutBlind(-slot_depth)
)
