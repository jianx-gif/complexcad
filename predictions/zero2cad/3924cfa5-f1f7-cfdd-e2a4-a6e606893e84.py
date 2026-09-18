import cadquery as cq

# Parameters
base_length = 80.0
base_width = 50.0
top_length = 60.0
top_width = 30.0
loft_height = 30.0
pocket_length = 30.0
pocket_width = 20.0
pocket_depth = 8.0
hole_diameter = 6.0
hole_clearance = 0.5
hole_spacing = 40.0
chamfer_size = 0.5

# Base lofted bracket
bracket = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .workplane(offset=loft_height)
    .rect(top_length, top_width)
    .loft()
)

# Recessed pocket on top face
bracket = (
    bracket
    .faces(">Z")
    .workplane()
    .rect(pocket_length, pocket_width)
    .cutBlind(-pocket_depth)
)

# Clearance holes on top face
hole_dia = hole_diameter + 2 * hole_clearance
bracket = (
    bracket
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
    .hole(hole_dia)
)

# Chamfer vertical edges for safety
bracket = bracket.edges("|Z").chamfer(chamfer_size)

result = bracket