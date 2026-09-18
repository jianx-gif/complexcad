import cadquery as cq

# Parameters
length = 80.0
width = 40.0
height = 20.0
wall_thickness = 4.0
rib_height = 6.0
rib_width = 8.0
rib_spacing = 12.0
hole_diameter = 12.0
chamfer_size = 1.0
pocket_depth = 4.0
pocket_width = 30.0
pocket_length = 30.0

# Base solid: rectangular block
base = cq.Workplane("XY").rect(width, height).extrude(length)

# Hollow interior to create wall thickness
inner = cq.Workplane("XY").rect(width - 2 * wall_thickness, height - 2 * wall_thickness).extrude(length)
result = base.cut(inner)

# Central through hole
result = result.faces(">Z").workplane().hole(hole_diameter)

# Chamfer outer vertical edges for safety
result = result.edges("|Z").chamfer(chamfer_size)

# Add ribs on +X side
num_ribs = int(length / rib_spacing) + 1
ribs_pos = (
    result.faces(">X").workplane()
    .rarray(0, rib_spacing, 1, num_ribs)
    .rect(rib_height, rib_width)
    .extrude(rib_width)
)
result = result.union(ribs_pos)

# Add ribs on -X side
ribs_neg = (
    result.faces("<X").workplane()
    .rarray(0, rib_spacing, 1, num_ribs)
    .rect(rib_height, rib_width)
    .extrude(rib_width)
)
result = result.union(ribs_neg)

# Add a recessed pocket on the +Y side for weight reduction
result = (
    result.faces(">Y").workplane()
    .center(0, length / 2)
    .rect(pocket_width, pocket_length)
    .cutBlind(-pocket_depth)
)
