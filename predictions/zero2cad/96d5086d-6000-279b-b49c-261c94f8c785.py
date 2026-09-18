import cadquery as cq

arm_length = 80.0
arm_width = 20.0
arm_thickness = 10.0
rib_height = 6.0
rib_width = 12.0
rib_length = 70.0
rib_offset = 5.0
hole_diameter = 6.0
counterbore_diameter = 10.0
counterbore_depth = 4.0
hole_offset = 20.0
chamfer_size = 0.5
boss_diameter = 10.0
boss_height = 4.0
slot_length = 20.0
slot_width = 6.0
slot_depth = 3.0

base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)

rib = (
    base.faces(">Z")
    .workplane()
    .center(-arm_length/2 + rib_offset + rib_length/2, 0)
    .rect(rib_length, rib_width)
    .extrude(rib_height)
)

boss = (
    rib.faces(">X")
    .workplane()
    .center(0, 0)
    .circle(boss_diameter/2)
    .extrude(boss_height)
)

slot = (
    boss.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-slot_depth)
)

hole = (
    slot.faces(">Z")
    .workplane()
    .center(-arm_length/2 + hole_offset, 0)
    .cboreHole(hole_diameter, counterbore_diameter, counterbore_depth)
)

result = (
    hole
    .edges("|Z and >X")
    .chamfer(chamfer_size)
)
