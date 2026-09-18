import cadquery as cq

# Parameters
total_length = 80.0
start_width = 20.0
end_width = 80.0
start_height = 10.0
end_height = 20.0
section_count = 8
section_height = total_length / section_count
slot_width = 2.0
slot_spacing = 10.0
slot_depth = 5.0
chamfer_distance = 0.5

# Build lofted body
loft_builder = cq.Workplane("XY").rect(start_width, start_height)
for i in range(1, section_count + 1):
    t = i / section_count
    w = start_width + t * (end_width - start_width)
    h = start_height + t * (end_height - start_height)
    loft_builder = loft_builder.workplane(offset=section_height).rect(w, h)
result = loft_builder.loft(combine=True)

# Chamfer top edges
result = result.faces(">Z").edges().chamfer(chamfer_distance)

# Add longitudinal slots on +Y face
num_slots = int(total_length / slot_spacing) + 1
result = (
    result.faces(">Y")
    .workplane()
    .rarray(slot_spacing, 0, num_slots, 1)
    .rect(slot_width, total_length)
    .cutBlind(-slot_depth)
)

# Add longitudinal slots on -Y face
result = (
    result.faces("<Y")
    .workplane()
    .rarray(slot_spacing, 0, num_slots, 1)
    .rect(slot_width, total_length)
    .cutBlind(-slot_depth)
)

# Add transverse slots on +X face
num_transverse = int(total_length / slot_spacing) + 1
result = (
    result.faces(">X")
    .workplane()
    .rarray(0, slot_spacing, 1, num_transverse)
    .rect(slot_width, total_length)
    .cutBlind(-slot_depth)
)

# Add transverse slots on -X face
result = (
    result.faces("<X")
    .workplane()
    .rarray(0, slot_spacing, 1, num_transverse)
    .rect(slot_width, total_length)
    .cutBlind(-slot_depth)
)
