import cadquery as cq
# Parameters
block_length = 80.0
block_width = 50.0
block_height = 30.0
wall_thickness = 3.0
chamfer_distance = 0.8
cap_radius = 15.0
cap_height = 8.0
pocket_length = 12.0
pocket_width = 8.0
pocket_depth = 15.0
pocket_spacing = 18.0
fillet_radius = 1.0
# Base profile with line and arc
base_profile = (cq.Workplane('XY')
    .moveTo(0, 0)
    .lineTo(block_length, 0)
    .lineTo(block_length, block_height - 10)
    .threePointArc((block_length/2, block_height + 5), (0, block_height - 10))
    .close())
# Extrude to create solid block
solid_block = base_profile.extrude(block_width)
# Chamfer vertical edges
chamfered_block = solid_block.edges("|Z").chamfer(chamfer_distance)
# Fillet external edges
filleted_block = chamfered_block.edges().fillet(fillet_radius)
# Create top cap as cylindrical extrusion
top_cap = (cq.Workplane('XY')
    .center(block_length/2, block_width/2)
    .circle(cap_radius)
    .extrude(cap_height)
    .translate((0, 0, block_height)))
# Union cap with block
combined_block = filleted_block.union(top_cap)
# Shell to create cavity (inner offset)
hollow_block = combined_block.shell(-wall_thickness)
# Add pocket array on front face (-Y direction)
result = (hollow_block.faces('<Y').workplane()
    .rect(pocket_length, pocket_width)
    .rarray(pocket_spacing, 0, 2, 1)
    .cutBlind(pocket_depth))
