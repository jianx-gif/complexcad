import cadquery as cq

# Parameters
shaft_diameter = 30.0
collar_outer_diameter = 70.0
collar_width = 20.0
relief_groove_depth = 8.0
relief_groove_length = 3.0
set_screw_diameter = 5.0
set_screw_width = 8.0
set_screw_depth = 12.0
chamfer_size = 1.0
seal_cap_height = 4.0
seal_cap_clearance = 0.5
seal_cap_diameter = shaft_diameter + 2 * seal_cap_clearance

r_outer = collar_outer_diameter / 2.0
r_inner = shaft_diameter / 2.0

# Base collar profile (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(r_outer, 0)
    .lineTo(r_outer, collar_width)
    .lineTo(r_outer - relief_groove_depth, collar_width)
    .lineTo(r_outer - relief_groove_depth, collar_width - relief_groove_length)
    .lineTo(r_inner, collar_width - relief_groove_length)
    .lineTo(r_inner, 0)
    .close()
)

# Revolve to create axisymmetric collar
base_collar = profile.revolve(360)

# Chamfer outer edges for safety
base_collar = base_collar.edges().chamfer(chamfer_size)

# Set screw pocket (radial slot) cut
pocket = (
    cq.Workplane("XY")
    .center(r_outer - set_screw_depth / 2.0, 0)
    .rect(set_screw_depth, set_screw_width)
    .extrude(collar_width)
)

collar_with_pocket = base_collar.cut(pocket)

# Seal cap (inner raised lip) union
seal_cap = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(seal_cap_diameter / 2.0)
    .extrude(seal_cap_height)
    .translate((0, 0, collar_width - seal_cap_height))
)

result = collar_with_pocket.union(seal_cap)
