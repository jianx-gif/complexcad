import cadquery as cq

# Parameters
arm_length = 80.0
arm_width = 30.0
arm_thickness = 8.0
rib_length = 40.0
rib_height = 2.0
hole_diameter = 6.0
hole_spacing = 15.0
hole_offset_from_end = 20.0
chamfer_size = 1.0
pocket_length = 25.0
pocket_width = 12.0
pocket_offset = 30.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)

# Central pocket cutout (through thickness)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(pocket_offset - arm_length/2, 0)
    .rect(pocket_length, pocket_width)
    .cutBlind(-arm_thickness)
)

# Reinforced rib on top surface, centered lengthwise
rib = (
    cq.Workplane("XY")
    .rect(rib_length, arm_width)
    .extrude(rib_height)
    .translate((0, 0, arm_thickness))
)

# Combine base and rib
combined = base.union(rib)

# Through holes pattern (three holes along length)
hole_positions = [
    -arm_length/2 + hole_offset_from_end,
    -arm_length/2 + hole_offset_from_end + hole_spacing,
    -arm_length/2 + hole_offset_from_end + 2*hole_spacing,
]
for x in hole_positions:
    combined = (
        combined
        .faces(">Z")
        .workplane()
        .center(x, 0)
        .hole(hole_diameter)
    )

# Chamfer outer vertical edges for safety
result = combined.edges("|Z").chamfer(chamfer_size)
