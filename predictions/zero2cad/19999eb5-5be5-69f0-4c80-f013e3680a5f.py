import cadquery as cq

# Parameters
bracket_length = 80.0
bracket_width = 50.0
bracket_thickness = 8.0
corner_radius = 4.0
slot_width = 12.0
slot_length = 20.0
slot_offset = 5.0
hole_diameter = 6.0
hole_depth = 5.0
hole_spacing = 30.0
rib_height = 4.0
rib_width = 8.0
rib_spacing = 15.0
chamfer_size = 1.0
shell_thickness = 1.0

# Base plate with rounded corners
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Chamfer outer edges for safety
base = base.edges().chamfer(chamfer_size)

# Slot cut on one side (centered along width)
slot_center_x = -bracket_length/2 + slot_offset + slot_length/2
base = (
    base.faces(">Z")
    .workplane()
    .center(slot_center_x, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-bracket_thickness)
)

# Blind holes pattern (two holes symmetric about center)
hole_y = 0
hole_x1 = -hole_spacing/2
hole_x2 = hole_spacing/2
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints([(hole_x1, hole_y), (hole_x2, hole_y)])
    .hole(hole_diameter, depth=hole_depth)
)

# Shell to create thin walls
shelled = base.shell(shell_thickness)

# Add ribs on the back face for stiffness
rib_face = shelled.faces("<Z")
rib_count = int((bracket_width - 2*corner_radius) // rib_spacing) + 1
rib_positions = [ -bracket_width/2 + corner_radius + i*rib_spacing for i in range(rib_count) ]
for y in rib_positions:
    rib = (
        rib_face.workplane()
        .center(0, y)
        .rect(rib_width, bracket_length - 2*corner_radius)
        .extrude(rib_height)
    )
    shelled = shelled.union(rib)

result = shelled