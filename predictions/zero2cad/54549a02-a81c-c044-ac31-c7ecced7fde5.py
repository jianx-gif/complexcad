import cadquery as cq

# Parameters
bracket_length = 70.0
bracket_width = 40.0
bracket_thickness = 10.0
gusset_height = 20.0
gusset_thickness = 8.0
slot_length = 50.0
slot_width = 10.0
hole_diameter = 6.0
hole_spacing = 30.0
hole_offset_y = 10.0
chamfer_distance = 2.0
rib_height = 6.0
rib_width = 8.0
rib_spacing = 12.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

# Gusset (triangular reinforcement) attached to +X side
gusset = (
    cq.Workplane("XY")
    .polyline([
        (bracket_length/2, -bracket_width/2),
        (bracket_length/2 + gusset_height, -bracket_width/2),
        (bracket_length/2, -bracket_width/2 + gusset_height),
    ])
    .close()
    .extrude(gusset_thickness)
)

# Combine base and gusset
result = base.union(gusset)

# Slot cut through the plate (centered)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .slot2D(slot_length, slot_width)
    .cutBlind(-bracket_thickness)
)

# Mounting holes (two holes symmetric about center line)
hole_positions = [(-hole_spacing/2, -hole_offset_y), (hole_spacing/2, -hole_offset_y)]
for x, y in hole_positions:
    result = (
        result.faces(">Z")
        .workplane()
        .center(x, y)
        .hole(hole_diameter)
    )

# Underside ribs for stiffness (array along length)
rib_count = int((bracket_length - rib_spacing) // rib_spacing) + 1
for i in range(rib_count):
    x_pos = -bracket_length/2 + rib_spacing/2 + i * rib_spacing
    rib = (
        cq.Workplane("XY")
        .center(x_pos, 0)
        .rect(rib_width, bracket_width)
        .extrude(rib_height)
        .translate((0, 0, -rib_height/2))
    )
    result = result.union(rib)

# Chamfer on the outer corner of the gusset (positive X, positive Y)
result = result.edges("|Z and >X and >Y").chamfer(chamfer_distance)
