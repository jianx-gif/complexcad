import cadquery as cq

# Parameters
outer_width = 80.0
outer_height = 60.0
outer_depth = 20.0
wall_thickness = 4.0
corner_radius = 5.0
central_hole_diameter = 20.0
tab_width = 40.0
tab_height = 8.0
chamfer_distance = 1.0

# Base block
base = (
    cq.Workplane("XY")
    .rect(outer_width, outer_height)
    .extrude(outer_depth)
)

# Rear mounting tab (attached to back side)
tab = (
    cq.Workplane("XY")
    .center(0, -outer_height/2 - tab_height/2)
    .rect(tab_width, tab_height)
    .extrude(outer_depth)
)

# Combine base and tab
combined = base.union(tab)

# Shell to create hollow interior
hollow = combined.shell(-wall_thickness)

# Fillet top outer edges for rounded corners
filleted = hollow.faces(">Z").edges().fillet(corner_radius)

# Chamfer bottom outer edges for safety
chamfered = filleted.faces("<Z").edges().chamfer(chamfer_distance)

# Central through hole
result = (
    chamfered
    .faces(">Z")
    .workplane()
    .hole(central_hole_diameter)
)
