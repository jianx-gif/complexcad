import cadquery as cq

# Parameters
bracket_length = 80.0
bracket_width = 30.0
bracket_thickness = 6.0
flange_height = 15.0
flange_thickness = 12.0
fillet_radius = 2.0
hole_diameter = 6.0
hole_offset_x = 20.0
hole_offset_y = 0.0
rib_height = 2.0
rib_width = 5.0
rib_length = bracket_length - 10.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

# Flange attached to the +Y side of the base
flange = (
    cq.Workplane("XY")
    .rect(bracket_length, flange_thickness)
    .extrude(flange_height)
    .translate((0, bracket_width/2 - flange_thickness/2, bracket_thickness))
)

# Combine base and flange
combined = base.union(flange)

# Apply fillet to all edges for safety
combined = combined.edges().fillet(fillet_radius)

# Add a reinforcing rib on the underside of the base
rib = (
    combined.faces("<Z")
    .workplane()
    .rect(rib_length, rib_width)
    .extrude(rib_height)
)
combined = combined.union(rib)

# Drill a through hole for a pin, positioned from the left edge
hole_center_x = -bracket_length/2 + hole_offset_x
hole_center_y = hole_offset_y
combined = (
    combined.faces(">Z")
    .workplane()
    .center(hole_center_x, hole_center_y)
    .hole(hole_diameter)
)

result = combined