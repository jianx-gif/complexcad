import cadquery as cq

# Parameters
block_length = 80.0
block_width = 50.0
block_height = 20.0
pocket_length = 40.0
pocket_width = 30.0
pocket_depth = 10.0
rib_height = 4.0
rib_thickness = 2.0
initial_chamfer = 1.0
mount_hole_dia = 4.0
mount_hole_offset = 12.0
bottom_boss_dia = 12.0
bottom_boss_height = 3.0
rib_fillet = 0.5

# Base block with chamfered edges
result = cq.Workplane('XY').box(block_length, block_width, block_height)
result = result.edges().chamfer(initial_chamfer)

# Central rectangular pocket cut into top face
result = (
    result.faces('>Z')
    .workplane()
    .rect(pocket_length, pocket_width)
    .cutBlind(-pocket_depth)
)

# Raised rib surrounding pocket
rib_outer_length = pocket_length + 2 * rib_thickness
rib_outer_width = pocket_width + 2 * rib_thickness
rib = (
    result.faces('>Z')
    .workplane()
    .rect(rib_outer_length, rib_outer_width)
    .extrude(rib_height)
)
rib = rib.edges('#Z and >Z').fillet(rib_fillet)
result = result.union(rib)

# Mounting holes on side faces (+X and -X)
for side in ['>X', '<X']:
    result = (
        result.faces(side)
        .workplane()
        .pushPoints([(0, mount_hole_offset), (0, -mount_hole_offset)])
        .hole(mount_hole_dia)
    )

# Bottom stand-off boss
result = (
    result.faces('<Z')
    .workplane()
    .circle(bottom_boss_dia / 2)
    .extrude(bottom_boss_height)
)
