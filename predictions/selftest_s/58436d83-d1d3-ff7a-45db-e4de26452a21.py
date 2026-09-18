import cadquery as cq

leaf_width = 80.0
leaf_length = 100.0
leaf_thickness = 8.0
boss_radius = 15.0
boss_height = 5.0
fastener_diameter = 5.0
fastener_depth = leaf_thickness + boss_height - 1.0
fastener_pattern_radius = 20.0
slot_width = 6.0
slot_length = 20.0
slot_offset = 5.0
rib_width = 4.0
rib_height = 3.0
rib_spacing = 12.0
chamfer_distance = 0.8

# Base leaf
leaf = (
    cq.Workplane('XY')
    .rect(leaf_width, leaf_length)
    .extrude(leaf_thickness)
)
# Central boss on top face
leaf = (
    leaf.faces('>Z')
    .workplane()
    .circle(boss_radius)
    .extrude(boss_height)
)
# Fastener holes through boss and leaf
fastener_positions = [
    (fastener_pattern_radius, 0),
    (-fastener_pattern_radius/2, fastener_pattern_radius*0.86602540378),
    (-fastener_pattern_radius/2, -fastener_pattern_radius*0.86602540378),
]
for x, y in fastener_positions:
    leaf = (
        leaf.faces('>Z')
        .workplane()
        .pushPoints([(x, y)])
        .hole(fastener_diameter, depth=fastener_depth)
    )
# Hinge pin slot on side face (positive Y edge)
slot_center_y = leaf_length/2 - slot_offset
leaf = (
    leaf.faces('>Y')
    .workplane()
    .center(0, slot_center_y)
    .rect(slot_width, slot_length)
    .cutBlind(-leaf_thickness)
)
# Ribs on back (negative Z) side, extruding outward
num_ribs = int((leaf_width - 2 * rib_spacing) // rib_spacing)
rib_array = (
    cq.Workplane('XY')
    .rect(rib_width, leaf_length)
    .rarray(rib_spacing, 0, num_ribs, 1)
    .extrude(-rib_height)
    .translate((-leaf_width/2 + rib_spacing/2, 0, 0))
)
leaf = leaf.union(rib_array)
# Chamfer outer top edges for safety
leaf = leaf.faces('>Z').edges().chamfer(chamfer_distance)
result = leaf
