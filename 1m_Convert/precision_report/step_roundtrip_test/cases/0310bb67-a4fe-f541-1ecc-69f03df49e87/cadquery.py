import cadquery as cq

# Parameters
cap_diameter = 80.0
cap_thickness = 10.0
bevel_chamfer = 2.0
pocket_radius = 30.0
pocket_depth = 3.0
hole_diameter = 6.0
hole_circle_radius = 15.0
hole_pattern_count = 6
boss_diameter = 15.0
boss_hole_diameter = 4.0
rib_height = 2.0
rib_width = 5.0
rib_offset_from_edge = 5.0
boss_fillet = 0.75

# Base cap
base = (
    cq.Workplane("XY")
    .circle(cap_diameter / 2)
    .extrude(cap_thickness)
)

# Central boss (mounting feature)
central_boss = (
    cq.Workplane("XY")
    .circle(boss_diameter / 2)
    .extrude(rib_height)
)

# Peripheral reinforcement rib (ring)
rib_outer_radius = (cap_diameter / 2) - rib_offset_from_edge
rib_inner_radius = rib_outer_radius - rib_width
peripheral_rib = (
    cq.Workplane("XY")
    .circle(rib_outer_radius)
    .circle(rib_inner_radius)
    .extrude(rib_height)
)

# Combine base, boss, and rib into a single solid
combined = base.union(central_boss).union(peripheral_rib)
combined = combined.edges().chamfer(bevel_chamfer)

# Recessed pocket cut
pocket = (
    cq.Workplane("XY")
    .circle(pocket_radius)
    .extrude(pocket_depth)
)
combined = combined.cut(pocket)

# Pattern of six holes within the recessed pocket
hole_tool = (
    cq.Workplane("XY")
    .rarray(hole_circle_radius, 0, hole_pattern_count, 1)
    .circle(hole_diameter / 2)
    .extrude(pocket_depth)
)
combined = combined.cut(hole_tool)

# Through hole for fastening through boss and cap
through_hole = (
    cq.Workplane("XY")
    .circle(boss_hole_diameter / 2)
    .extrude(cap_thickness + rib_height * 2)
)
combined = combined.cut(through_hole)

# Fillet on the top edge of the central boss for handling
combined = combined.faces(">Z").edges().fillet(boss_fillet)

result = combined
