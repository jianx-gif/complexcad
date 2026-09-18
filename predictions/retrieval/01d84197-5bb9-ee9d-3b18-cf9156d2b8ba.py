import cadquery as cq

cap_outer_diameter = 80.0
cap_height = 30.0
wall_thickness = 5.0
slot_width = 12.0
slot_length = 30.0
slot_depth = 8.0
fillet_radius = 3.0
hole_diameter = 6.0
hole_spacing = 40.0
rib_width = 10.0
rib_height = 6.0
rib_offset = 5.0

cap_outer_radius = cap_outer_diameter / 2.0

# Base solid cylinder
cylinder = cq.Workplane('XY').circle(cap_outer_radius).extrude(cap_height)

# Create thin-walled cap by shelling
cap_body = cylinder.shell(-wall_thickness)

# Apply fillet to the rim (top edge)
cap_body = cap_body.faces('>Z').edges().fillet(fillet_radius)

# Top mounting holes (through the cap)
cap_body = (
    cap_body
    .faces('>Z')
    .workplane()
    .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
    .hole(hole_diameter)
)

# Reinforcing rib on top face, offset from center
rib = (
    cap_body
    .faces('>Z')
    .workplane()
    .center(rib_offset, 0)
    .rect(rib_width, rib_width)
    .extrude(rib_height)
)

cap_body = cap_body.union(rib)

# Recessed rectangular slot on the +Y side face
cap_body = (
    cap_body
    .faces('>Y')
    .workplane(invert=True)
    .center(0, cap_height/2 - slot_length/2)
    .rect(slot_width, slot_length)
    .cutBlind(-slot_depth)
)

result = cap_body
