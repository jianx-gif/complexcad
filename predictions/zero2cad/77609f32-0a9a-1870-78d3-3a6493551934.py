import cadquery as cq

# Parameters
arm_length = 80.0
arm_width = 20.0
arm_thickness = 8.0
tab_length = 30.0
tab_width = 12.0
slot_length = 25.0
slot_width = 6.0
slot_depth = 4.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 3
chamfer_size = 0.8
rib_length = 50.0
rib_width = 6.0
rib_height = 4.0

# Base arm solid
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)

# Tab solid attached to the +X side of the arm
tab = (
    cq.Workplane("XY")
    .center(arm_length / 2 + tab_length / 2, 0)
    .rect(tab_length, tab_width)
    .extrude(arm_thickness)
)

# Combine base and tab
result = base.union(tab)

# Recessed slot on the top surface of the arm (centered along length)
result = (
    result.faces(">Z")
    .workplane()
    .center(arm_length / 2, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-slot_depth)
)

# Pattern of three through holes on the top surface of the tab
result = (
    result.faces(">Z")
    .workplane()
    .center(arm_length / 2 + tab_length / 2, 0)
    .rarray(hole_spacing, 0, hole_count, 1)
    .hole(hole_diameter)
)

# Reinforcing rib on the underside of the arm
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_length, rib_width)
    .extrude(rib_height)
    .translate((0, 0, -rib_height))
)
result = result.union(rib)

# Chamfer outer edges on the top face for safety
result = result.faces(">Z").edges().chamfer(chamfer_size)
