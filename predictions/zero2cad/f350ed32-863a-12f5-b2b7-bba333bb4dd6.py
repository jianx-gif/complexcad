import cadquery as cq

# Parameters
bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 8.0
rib_width = 30.0
rib_height = 12.0
rib_thickness = 3.0
slot_width = 6.0
slot_length = 60.0
fillet_radius = 1.5
chamfer_distance = 0.7
hole_diameter = 4.0
hole_offset_x = 25.0
hole_offset_y = 12.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

# Central rib on top face
rib = (
    base.faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)

# Combine base and rib
combined = base.union(rib)

# Slot cut through the combined part (centered)
slot_cut = (
    combined.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_length)
    .cutBlind(-bracket_thickness)
)

# Fillet the slot ends (edges parallel to Y on the top face)
filleted = (
    slot_cut.edges("|Y and >Z")
    .fillet(fillet_radius)
)

# Chamfer outer top edges for safety
chamfered = (
    filleted.edges(">Z")
    .chamfer(chamfer_distance)
)

# Add mounting holes on the top face, symmetric about center
holes = (
    chamfered.faces(">Z")
    .workplane()
    .pushPoints([(-hole_offset_x, -hole_offset_y), (hole_offset_x, -hole_offset_y)])
    .hole(hole_diameter)
)

result = holes