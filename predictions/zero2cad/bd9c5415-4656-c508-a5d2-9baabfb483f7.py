import cadquery as cq

# Parameters
base_width = 60.0
base_height = 40.0
base_thickness = 12.0
flange_length = 30.0
flange_thickness = 12.0
flange_width = 15.0
fillet_radius = 3.0
hole_diameter = 6.0
hole_spacing = 20.0
rib_width = 8.0
rib_height = 8.0
rib_thickness = 3.0
pocket_width = 20.0
pocket_depth = 6.0

# Base block
base = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(base_thickness)
)

# Flange attached to +X side of base
flange = (
    base.faces(">X")
    .workplane()
    .rect(flange_thickness, flange_length)
    .extrude(flange_width)
)

# Combine base and flange
combined = base.union(flange)

# Fillet on the outer edge of the flange (edges parallel to Y on the +X side)
combined = combined.edges("|Y and >X").fillet(fillet_radius)

# Add a central pocket on the top face for weight reduction
combined = (
    combined.faces(">Z")
    .workplane()
    .rect(pocket_width, base_height - 2 * fillet_radius)
    .cutBlind(-pocket_depth)
)

# Add a reinforcing rib on the bottom face
combined = (
    combined.faces("<Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)

# Drill three through holes on the top face, spaced along X axis
hole_positions = [(-hole_spacing, 0), (0, 0), (hole_spacing, 0)]
combined = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

result = combined