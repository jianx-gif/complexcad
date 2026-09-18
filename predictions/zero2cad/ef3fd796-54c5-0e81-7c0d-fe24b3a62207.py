import cadquery as cq

# Parameters
bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 5.0
rib_height = 3.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
fillet_radius = 1.5
chamfer_distance = 0.8

# Base plate
base = (
    cq.Workplane("XY")
    .rect(bracket_width, bracket_length)
    .extrude(bracket_thickness)
)

# Rib pattern on top face
rib_count = int((bracket_length - rib_spacing) // rib_spacing) + 1
rib_pattern = (
    base.faces(">Z")
    .workplane()
    .rarray(rib_spacing, 0, rib_count, 1, center=True)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)

# Combine base and ribs
bracket = base.union(rib_pattern)

# Through holes on the +X side face
hole_positions = [
    (-bracket_width/2 + hole_spacing, 0),
    (0, 0),
    (bracket_width/2 - hole_spacing, 0)
]
bracket = (
    bracket.faces(">X")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

# Fillet outer vertical edges
bracket = bracket.edges("|Z").fillet(fillet_radius)

# Chamfer edges on the +X side face for safety
bracket = bracket.faces(">X").edges().chamfer(chamfer_distance)

result = bracket