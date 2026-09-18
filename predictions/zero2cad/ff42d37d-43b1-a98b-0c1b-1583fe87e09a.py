import cadquery as cq

# Parameters
bracket_length = 60.0
bracket_width = 30.0
bracket_thickness = 8.0
pocket_length = 30.0
pocket_width = 15.0
pocket_depth = 6.0
slot_length = 20.0
slot_width = 8.0
slot_offset = 5.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
fillet_radius = 0.8
rib_length = 20.0
rib_width = 10.0
rib_height = 8.0

# Base plate
result = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

# Central pocket cut
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(pocket_length, pocket_width)
    .cutBlind(-pocket_depth)
)

# Side slot cut
result = (
    result.faces(">Z")
    .workplane()
    .center(-bracket_length/2 + slot_offset + slot_length/2, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-bracket_thickness)
)

# Mounting holes pattern (two holes along width)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, -hole_spacing/2)
    .hole(hole_diameter)
    .center(0, hole_spacing)
    .hole(hole_diameter)
)

# Reinforcing rib on top surface
result = (
    result.faces(">Z")
    .workplane()
    .center(bracket_length/2 - rib_length/2, 0)
    .rect(rib_length, rib_width)
    .extrude(rib_height)
)

# Fillet vertical edges for safety
result = result.edges("|Z").fillet(fillet_radius)
