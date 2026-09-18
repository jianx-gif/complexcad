import cadquery as cq

# Parameters
outer_length = 80.0
outer_width = 40.0
outer_height = 20.0
wall_thickness = 2.0
entry_radius = 5.0
entry_depth = 12.0
rib_width = 4.0
rib_thickness = 2.0
rib_height = outer_height - 2 * wall_thickness
fillet_radius = 0.8
chamfer_dist = 0.5

# Base block (composite sketch rectangle)
base = (
    cq.Workplane("XY")
    .rect(outer_length, outer_width)
    .extrude(outer_height)
)

# Create hollow interior via shell
hollow = base.shell(-wall_thickness)

# Add internal support rib from interior bottom
rib = (
    hollow
    .faces("<Z")
    .workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)

combined = hollow.union(rib)

# Recessed cylindrical cable entry on +Y side
entry_cut = (
    combined
    .faces(">Y")
    .workplane()
    .center(0, outer_height/2)
    .circle(entry_radius)
    .cutBlind(entry_depth)
)

# Fillet outer vertical edges
filleted = entry_cut.edges("|Z").fillet(fillet_radius)

# Chamfer the edge of the entry pocket on the +Y face
result = filleted.faces(">Y").edges().chamfer(chamfer_dist)
