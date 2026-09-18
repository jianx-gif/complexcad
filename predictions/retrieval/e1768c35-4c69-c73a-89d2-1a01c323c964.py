import cadquery as cq

outer_radius = 35
wall_thickness = 5
inner_radius = outer_radius - wall_thickness
cap_height = 20
chamfer_size = 3
set_screw_dia = 4
counterbore_dia = 8
counterbore_depth = 4
slot_thickness = 2
slot_height = 10
slot_spacing = 12
slot_count = 2

# Base quarter cylinder cap
base = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, cap_height)
    .lineTo(inner_radius, cap_height)
    .close()
    .revolve(90)
)

# Add slots on outer curved face (cutting into wall)
solid = (
    base
    .faces(">X")
    .workplane()
    .rarray(slot_spacing, 0, slot_count, 1)
    .rect(slot_thickness, slot_height)
    .cutBlind(-slot_thickness)
)

# Apply 60° chamfer on outer top edge
solid = solid.edges("|Z and >X").chamfer(chamfer_size)

# Set screw hole oriented at 45° through the inner corner
hole = (
    cq.Workplane("XY")
    .transformed(rotate=(0, 45, 0), offset=(inner_radius, 0, cap_height/2))
    .circle(set_screw_dia/2)
    .extrude(-cap_height)
)

# Counterbore at the entry of the set screw hole (top surface)
counterbore = (
    cq.Workplane("XY")
    .transformed(rotate=(0, 45, 0), offset=(inner_radius, 0, cap_height))
    .circle(counterbore_dia/2)
    .extrude(-counterbore_depth)
)

result = solid.cut(hole).cut(counterbore)

assert result.val().Volume() > 0
