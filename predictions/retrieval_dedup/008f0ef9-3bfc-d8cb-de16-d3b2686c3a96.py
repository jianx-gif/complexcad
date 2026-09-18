import cadquery as cq

# Parameters
block_length = 80.0
block_width = 60.0
block_height = 15.0
pocket_diameter = 30.0
pocket_depth = 12.0
chamfer_distance = 1.0
bolt_hole_diameter = 5.0
bolt_spacing_x = 50.0
bolt_spacing_y = 40.0
rib_thickness = 5.0
rib_height = 4.0
rib_offset = 12.0
slot_length = 20.0
slot_width = 8.0

# Base block
result = (
    cq.Workplane('XY')
    .rect(block_length, block_width)
    .extrude(block_height)
)

# Side slots (cut through full thickness)
result = (
    result.faces('>Z')
    .workplane()
    .center(-block_length/2 + slot_length/2, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-block_height)
)
result = (
    result.faces('>Z')
    .workplane()
    .center(block_length/2 - slot_length/2, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-block_height)
)

# Central cylindrical pocket
pocket = (
    cq.Workplane('XY')
    .center(0, 0)
    .circle(pocket_diameter/2)
    .extrude(pocket_depth)
)
result = result.cut(pocket)

# Chamfer on all vertical edges
result = result.edges('|Z').chamfer(chamfer_distance)

# Bolt hole pattern (4 holes rectangular)
bolt_positions = [
    ( bolt_spacing_x/2,  bolt_spacing_y/2),
    (-bolt_spacing_x/2,  bolt_spacing_y/2),
    (-bolt_spacing_x/2, -bolt_spacing_y/2),
    ( bolt_spacing_x/2, -bolt_spacing_y/2),
]
for x, y in bolt_positions:
    result = (
        result.faces('>Z')
        .workplane()
        .center(x, y)
        .hole(bolt_hole_diameter)
    )

# Reinforcing ribs on top surface (two parallel ribs)
rib1 = (
    cq.Workplane('XY')
    .center(-block_length/2 + rib_offset, 0)
    .rect(rib_thickness, block_width - 2*rib_offset)
    .extrude(rib_height)
)
rib2 = (
    cq.Workplane('XY')
    .center(block_length/2 - rib_offset, 0)
    .rect(rib_thickness, block_width - 2*rib_offset)
    .extrude(rib_height)
)
result = result.union(rib1).union(rib2)
