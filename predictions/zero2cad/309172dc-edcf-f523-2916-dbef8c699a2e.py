import cadquery as cq

# Parameters
base_radius = 20.0
top_side = 30.0
height = 60.0
wall_thickness = 2.0
fillet_radius = 1.5
chamfer_distance = 0.5
rib_width = 8.0
rib_height = 3.0
rib_spacing = 20.0
rib_count = 2

# Outer lofted shape
outer = (
    cq.Workplane("XY")
    .circle(base_radius)
    .workplane(offset=height)
    .rect(top_side, top_side)
    .loft(combine=True)
)

# Inner lofted shape (offset for wall thickness)
inner = (
    cq.Workplane("XY")
    .circle(base_radius - wall_thickness)
    .workplane(offset=height)
    .rect(top_side - 2 * wall_thickness, top_side - 2 * wall_thickness)
    .loft(combine=True)
)

# Hollow shell
shell = outer.cut(inner)

# Add ribs on the bottom face
ribs = (
    shell.faces("<Z")
    .workplane()
    .rarray(rib_spacing, 0, rib_count, 1)
    .rect(rib_width, height)
    .extrude(rib_height)
)

# Combine ribs with shell
combined = shell.union(ribs)

# Apply fillet to vertical edges
filleted = combined.edges("|Z").fillet(fillet_radius)

# Apply chamfer to horizontal edges
result = filleted.edges("|X").chamfer(chamfer_distance)
