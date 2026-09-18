import cadquery as cq

# Parameters
arm_length = 80.0
arm_width = 30.0
arm_thickness = 10.0
rib_width = 12.0
rib_height = 6.0
slot_width = 6.0
slot_length = 20.0
num_slots = 3
slot_spacing = (arm_length - (num_slots * slot_length)) / (num_slots + 1)
fillet_radius = 4.0
chamfer_distance = 1.0

total_thickness = arm_thickness + rib_height

# Base plate
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)

# Central rib (raised on top of base)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(arm_length, rib_width)
    .extrude(rib_height)
    .translate((0, 0, arm_thickness))
)

# Combine base and rib
part = base.union(rib)

# Perforated slots (through full thickness)
for i in range(num_slots):
    x_offset = -arm_length/2 + slot_spacing * (i + 1) + slot_length * i + slot_length/2
    slot = (
        cq.Workplane("XY", origin=(0, 0, total_thickness))
        .center(x_offset, 0)
        .rect(slot_length, slot_width)
        .extrude(-total_thickness)
    )
    part = part.cut(slot)

# Fillet on the leading (+X) face edges for smooth pivoting
part = part.faces(">X").edges().fillet(fillet_radius)

result = part