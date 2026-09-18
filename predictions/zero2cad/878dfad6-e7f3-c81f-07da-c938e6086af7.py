import cadquery as cq

# Parameters
bracket_length = 60.0
bracket_width = 30.0
bracket_thickness = 8.0
slot_length = 45.0
slot_width = 6.0
slot_offset_y = 0.0
boss_diameter = 12.0
boss_height = 6.0
boss_recess_depth = 3.0
boss_offset_x = 0.0
boss_offset_y = 0.0
chamfer_size = 0.5
rib_thickness = 3.0
rib_height = 4.0
rib_spacing = 10.0
mount_hole_dia = 4.0
mount_hole_spacing = 20.0
mount_hole_offset_y = 10.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

# Slot cut through the plate
slot = (
    cq.Workplane("XY")
    .center(0, slot_offset_y)
    .rect(slot_length, slot_width)
    .extrude(bracket_thickness + 1)
)
base = base.cut(slot)

# Recessed boss (cylindrical protrusion with recessed pocket)
# Boss cylinder
boss = (
    cq.Workplane("XY")
    .center(boss_offset_x, boss_offset_y)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)
# Recessed pocket (cut into boss)
recess = (
    cq.Workplane("XY")
    .center(boss_offset_x, boss_offset_y)
    .circle((boss_diameter - 2) / 2)
    .extrude(boss_recess_depth)
)
base = base.union(boss).cut(recess)

# Mounting holes (two holes symmetric about center line)
hole_positions = [
    (-mount_hole_spacing / 2, mount_hole_offset_y),
    (mount_hole_spacing / 2, mount_hole_offset_y),
]
for x, y in hole_positions:
    base = (
        base.faces("<Z")
        .workplane(centerOption="CenterOfMass")
        .center(x, y)
        .hole(mount_hole_dia)
    )

# Ribs on top surface for stiffness (grid pattern)
num_ribs_x = int((bracket_length - 2 * rib_spacing) // rib_spacing)
num_ribs_y = int((bracket_width - 2 * rib_spacing) // rib_spacing)
for i in range(num_ribs_x):
    for j in range(num_ribs_y):
        x = -bracket_length / 2 + rib_spacing + i * rib_spacing
        y = -bracket_width / 2 + rib_spacing + j * rib_spacing
        rib = (
            cq.Workplane("XY")
            .center(x, y)
            .rect(rib_thickness, rib_thickness)
            .extrude(rib_height)
        )
        base = base.union(rib)

# Chamfer outer edges for safety
result = base.edges(">Z").chamfer(chamfer_size)
