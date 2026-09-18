import cadquery as cq

# Parameters
cover_width = 80.0
cover_length = 60.0
cover_thickness = 5.0
wall_thickness = 2.0
rib_height = 2.0
rib_width = 4.0
rib_spacing = 6.0
hole_diameter = 3.0
hole_rows = 3
hole_cols = 4
hole_spacing_x = 15.0
hole_spacing_y = 12.0
edge_chamfer = 0.5

# Base outer solid
outer = cq.Workplane('XY').box(cover_width, cover_length, cover_thickness)

# Inner cavity (hollow interior)
inner = (
    cq.Workplane('XY')
    .box(cover_width - 2 * wall_thickness,
         cover_length - 2 * wall_thickness,
         cover_thickness - wall_thickness)
    .translate((0, 0, wall_thickness / 2))
)

# Subtract inner cavity and chamfer outer vertical edges
cover_body = outer.cut(inner).edges('|Z').chamfer(edge_chamfer)

# Effective dimensions for rib placement
effective_width = cover_width - 2 * wall_thickness
effective_length = cover_length - 2 * wall_thickness
ribs_per_side_x = int((effective_length + rib_spacing) // (rib_width + rib_spacing))
ribs_per_side_y = int((effective_width + rib_spacing) // (rib_width + rib_spacing))

# Positions for ribs along +X and -X edges (ribs oriented along Y)
start_y = -effective_length / 2 + rib_width / 2
y_positions = [start_y + i * (rib_width + rib_spacing) for i in range(ribs_per_side_x)]

# Ribs on +X edge (slightly intersect base for merging)
rib_plus_x = (
    cover_body.faces('>Z')
    .workplane(offset=-0.01)
    .pushPoints([(cover_width / 2 - wall_thickness - rib_width / 2, y) for y in y_positions])
    .rect(rib_width, rib_width)
    .extrude(rib_height)
)
# Ribs on -X edge
rib_minus_x = (
    cover_body.faces('>Z')
    .workplane(offset=-0.01)
    .pushPoints([(-cover_width / 2 + wall_thickness + rib_width / 2, y) for y in y_positions])
    .rect(rib_width, rib_width)
    .extrude(rib_height)
)

# Positions for ribs along +Y and -Y edges (ribs oriented along X)
start_x = -effective_width / 2 + rib_width / 2
x_positions = [start_x + i * (rib_width + rib_spacing) for i in range(ribs_per_side_y)]

# Ribs on +Y edge
rib_plus_y = (
    cover_body.faces('>Z')
    .workplane(offset=-0.01)
    .pushPoints([(x, cover_length / 2 - wall_thickness - rib_width / 2) for x in x_positions])
    .rect(rib_width, rib_width)
    .extrude(rib_height)
)
# Ribs on -Y edge
rib_minus_y = (
    cover_body.faces('>Z')
    .workplane(offset=-0.01)
    .pushPoints([(x, -cover_length / 2 + wall_thickness + rib_width / 2) for x in x_positions])
    .rect(rib_width, rib_width)
    .extrude(rib_height)
)

# Combine ribs and merge with cover body
ribs = rib_plus_x.union(rib_minus_x).union(rib_plus_y).union(rib_minus_y)
result = cover_body.union(ribs)

# Add mounting holes pattern on top face
result = (
    result.faces('>Z')
    .workplane()
    .rarray(hole_spacing_x, hole_spacing_y, hole_cols, hole_rows)
    .hole(hole_diameter)
)
