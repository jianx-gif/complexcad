import cadquery as cq

arm_length = 80.0
arm_width = 30.0
arm_thickness = 12.0
rib_width = 4.0
rib_height = 6.0
rib_spacing = 8.0
rib_count = 6
rib_depth = 3.0
slot_width = 6.0
slot_height = 8.0
slot_spacing = 12.0
slot_count = 4
chamfer_distance = 2.0

# Base lever arm
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)

# Rib side on +Y face
ribs = (
    base.faces(">Y")
    .workplane()
    .rect(rib_width, rib_height)
    .rarray(rib_spacing, 0, rib_count, 1)
    .extrude(rib_depth)
)

lever_with_ribs = base.union(ribs)

# Ventilation slots on -Y face (cut through thickness)
slots = (
    lever_with_ribs.faces("<Y")
    .workplane(offset=arm_thickness/2)
    .rect(slot_width, slot_height)
    .rarray(slot_spacing, 0, slot_count, 1)
    .cutBlind(-arm_thickness)
)

# Chamfer tip on +X end
result = (
    slots
    .faces(">X")
    .edges()
    .chamfer(chamfer_distance)
)
