import cadquery as cq

# Parameters
plate_length = 80.0
plate_width = 40.0
plate_thickness = 5.0
rib_height = 3.0
rib_thickness = 2.0
rib_edge_clearance = 4.0
hex_radius = 6.0
hex_height = 6.0
hole_diameter = 5.0
counterbore_diameter = 9.0
counterbore_depth = 3.0
hole_count = 6
edge_chamfer = 0.5
edge_margin = 8.0
intersect_depth = 0.5

# Base plate
result = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

# Top ribs (create separate, translate to intersect, then fuse)
rib_length = plate_length - 2 * rib_edge_clearance
top_rib = (
    cq.Workplane()
    .center(0, (plate_width/2) - rib_thickness/2 - rib_edge_clearance/2)
    .rect(rib_length, rib_thickness)
    .extrude(rib_height)
    .translate((0, 0, -intersect_depth))
)
result = result.union(top_rib)

# Bottom ribs (translate upward to intersect)
bottom_rib = (
    cq.Workplane()
    .center(0, -(plate_width/2) + rib_thickness/2 + rib_edge_clearance/2)
    .rect(rib_length, rib_thickness)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness - rib_height + intersect_depth))
)
result = result.union(bottom_rib)

# Central hexagonal boss (translate down to intersect base)
hex_boss = (
    cq.Workplane()
    .polygon(6, 2*hex_radius)
    .extrude(hex_height)
    .translate((0, 0, -intersect_depth))
)
result = result.union(hex_boss)

# Counterbored holes array on top surface (cut material)
hole_spacing = (plate_length - 2*edge_margin) / (hole_count - 1)
result = (
    result.faces(">Z").workplane()
    .rarray(hole_spacing, 0, hole_count, 1)
    .hole(counterbore_diameter, depth=counterbore_depth)
    .hole(hole_diameter, depth=plate_thickness + hex_height)
)

# Chamfer outer edges
result = result.edges("|Z").chamfer(edge_chamfer)
