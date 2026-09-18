import cadquery as cq

arm_length = 80.0
arm_width = 20.0
arm_thickness = 10.0
flange_width = 35.0
flange_thickness = 6.0
rib_width = 4.0
rib_height = 12.0
rib_depth = 3.0
rib_spacing = 12.0
hole_diameter = 5.0
countersink_diameter = 9.0
countersink_angle = 45.0
chamfer_size = 1.0
boss_diameter = 10.0
boss_length = 20.0
slot_width = 4.0
slot_length = 30.0

base = (
    cq.Workplane("YZ")
    .rect(arm_width, arm_thickness)
    .extrude(arm_length)
)

flange = (
    cq.Workplane("YZ")
    .rect(flange_width, flange_thickness)
    .extrude(arm_length)
    .translate((0, 0, arm_thickness / 2 + flange_thickness / 2))
)

result = base.union(flange)

rib_count = int(arm_length / rib_spacing) + 1
ribs = (
    result.faces("<Y")
    .workplane()
    .rarray(rib_spacing, 0, rib_count, 1)
    .rect(rib_width, rib_height)
    .extrude(-rib_depth)
)
result = result.union(ribs)

result = (
    result.faces(">Z")
    .workplane()
    .cskHole(hole_diameter, countersink_diameter, countersink_angle)
)

result = result.faces(">Z").edges().chamfer(chamfer_size)

boss = (
    result.faces(">Y")
    .workplane()
    .center(arm_length / 2, 0)
    .circle(boss_diameter / 2)
    .extrude(boss_length)
)
result = result.union(boss)

result = (
    result.faces("<Y")
    .workplane()
    .center(arm_length / 2, 0)
    .rect(slot_width, slot_length)
    .cutBlind(-arm_thickness / 2)
)
