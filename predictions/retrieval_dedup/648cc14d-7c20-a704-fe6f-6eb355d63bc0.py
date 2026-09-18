import cadquery as cq

bracket_length = 70
bracket_width = 30
bracket_thickness = 8
gusset_height = 15
gusset_thickness = 5
hole_diameter = 5
hole_spacing = 20
hole_edge_margin = 10
chamfer_size = 1.5

# Base plate
base = cq.Workplane('XY').rect(bracket_length, bracket_width).extrude(bracket_thickness)

# Gusset: triangular prism attached to the positive X side, centered in Y
gusset = (
    cq.Workplane('YZ')
    .center(bracket_thickness / 2, 0)
    .polyline([
        (0, -gusset_height / 2),
        (gusset_thickness, 0),
        (0, gusset_height / 2),
        (0, -gusset_height / 2)
    ])
    .close()
    .extrude(gusset_thickness)
    .translate((bracket_length / 2, 0, 0))
)

# Combine base and gusset
combined = base.union(gusset)

# Hole pattern on top face
hole_positions = [hole_edge_margin + i * hole_spacing for i in range(6)]
combined = (
    combined.faces('>Z').workplane()
    .pushPoints([(x - bracket_length / 2, 0) for x in hole_positions])
    .hole(hole_diameter)
)

# Chamfer inner vertical edge (inner side of bracket)
result = combined.edges("|Z and <X").chamfer(chamfer_size)
