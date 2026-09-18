import cadquery as cq
leaf_width = 80.0
leaf_length = 100.0
leaf_thickness = 8.0
boss_radius = 15.0
boss_height = 5.0
slot_width = 6.0
slot_length = 20.0
slot_offset = 5.0
slot_count = 4
slot_depth = leaf_thickness - 2.0
chamfer_distance = 0.8
base = (
    cq.Workplane("XY")
    .rect(leaf_width, leaf_length)
    .extrude(leaf_thickness)
)
boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(boss_radius)
    .extrude(boss_height)
)
leaf = base.union(boss)
leaf = (
    leaf.faces(">Z")
    .workplane()
    .center(0, leaf_length/2 - boss_height/2)
    .rect(slot_width, slot_length)
    .cutBlind(-leaf_thickness)
)
leaf = (
    leaf.faces(">Z")
    .workplane()
    .center(0, leaf_length/2 - boss_height/2)
    .rect(slot_width, leaf_length)
    .cutBlind(-leaf_thickness)
)
result = leaf
