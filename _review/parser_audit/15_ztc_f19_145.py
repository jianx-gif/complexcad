import cadquery as cq

arm_length = 100.0
arm_width = 30.0
arm_thickness = 10.0
keyway_slot_length = 80.0
keyway_slot_width = 4.0
keyway_slot_spacing = 12.0
num_keyway_slots = 5
total_slot_span = (num_keyway_slots - 1) * keyway_slot_spacing
fillet_radius = 3.0
chamfer_distance = 0.5
rib_width = 5.0
rib_offset = 2.0
rib_length = 80.0
mounting_hole_diameter = 6.0
mounting_hole_spacing = 40.0

base = (
    cq.Workplane("XY")
    .rect(arm_width, arm_thickness)
    .extrude(arm_length)
)

base = (
    base.faces(">Y")
    .workplane()
    .center(-total_slot_span / 2.0, 0)
    .rarray(keyway_slot_spacing, 0, num_keyway_slots, 1)
    .rect(keyway_slot_width, keyway_slot_length)
    .cutBlind(-arm_thickness)
)

rib1 = (
    cq.Workplane("XY")
    .center(-arm_width / 2.0 + rib_offset + rib_width / 2.0, 0)
    .rect(rib_width, arm_thickness)
    .extrude(rib_length)
)

rib2 = (
    cq.Workplane("XY")
    .center(arm_width / 2.0 - rib_offset - rib_width / 2.0, 0)
    .rect(rib_width, arm_thickness)
    .extrude(rib_length)
)

rib1 = rib1.edges().chamfer(chamfer_distance)
rib2 = rib2.edges().chamfer(chamfer_distance)

base = base.union(rib1).union(rib2)

hole_positions = [(-mounting_hole_spacing / 2.0, 0), (mounting_hole_spacing / 2.0, 0)]
base = (
    base.faces("<Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mounting_hole_diameter)
)

base = base.faces(">Z").edges().fillet(fillet_radius)

result = base