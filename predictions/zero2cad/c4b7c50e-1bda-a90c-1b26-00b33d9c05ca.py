import cadquery as cq

# Parameters
outer_size = 80.0
wall_thickness = 2.0
length = 100.0
rib_width = 10.0
rib_height = 5.0
hole_diameter = 5.0
countersink_diameter = 8.0
countersink_angle = 82.0
hole_spacing = 30.0
chamfer_size = 1.0

# Base solid: square tube
base = (
    cq.Workplane("XY")
    .rect(outer_size, outer_size)
    .extrude(length)
    .shell(-wall_thickness)
)

# Central rib on top face
rib = (
    base.faces(">Z")
    .workplane()
    .rect(outer_size, rib_width)
    .extrude(rib_height)
)

# Combine base and rib
combined = base.union(rib)

# Countersunk holes on +X face
holes_pos = (
    combined.faces(">X")
    .workplane()
    .rarray(0, hole_spacing, 1, 3)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle, wall_thickness + 0.5)
)

# Countersunk holes on -X face
holes_neg = (
    holes_pos.faces("<X")
    .workplane()
    .rarray(0, hole_spacing, 1, 3)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle, wall_thickness + 0.5)
)

# Chamfer outer edges
result = (
    holes_neg.edges("|Z or >X or <X")
    .chamfer(chamfer_size)
)
