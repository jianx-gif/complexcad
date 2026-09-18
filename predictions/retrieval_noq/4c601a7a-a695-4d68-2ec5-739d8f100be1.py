import cadquery as cq

# Parameters
arm_length = 80.0
arm_width = 30.0
arm_thickness = 8.0
pivot_radius = 5.0
clearance_hole_diam = 4.0
hole_spacing = 20.0
chamfer_dist = 2.0
rib_height = 4.0
rib_width = 12.0
cable_slot_width = 6.0
cable_slot_depth = 3.0
counterbore_diam = 6.0
counterbore_depth = 2.0
pocket_width = 10.0
pocket_length = 20.0
pocket_depth = 2.0

# Base solid
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)
# Rib solid positioned on top edge
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(arm_thickness)
    .translate((0, (arm_width / 2) + (rib_height / 2), 0))
)
# Composite profile
result = base.union(rib)

# Chamfer rear vertical edges for safety before other features
result = result.edges("<X and |Z").chamfer(chamfer_dist)

# Rear clearance hole for pivot pin (through entire thickness)
result = (
    result.faces("<X")
    .workplane()
    .hole(pivot_radius * 2)
)

# Front linear array of two clearance holes (through thickness)
result = (
    result.faces(">X")
    .workplane()
    .center(-hole_spacing / 2, 0)
    .hole(clearance_hole_diam)
    .center(hole_spacing, 0)
    .hole(clearance_hole_diam)
)

# Cable slot cut from top surface, depth limited to half thickness
result = (
    result.faces("<Z")
    .workplane()
    .center(0, 0)
    .rect(cable_slot_width, arm_width * 0.6)
    .cutBlind(-cable_slot_depth)
)

# Counterbore on top surface near rib for mounting bolt
cb_x = 0
cb_y = (arm_width / 2) + (rib_height / 4)
result = (
    result.faces("+Z")
    .workplane()
    .center(cb_x, cb_y)
    .hole(counterbore_diam, depth=counterbore_depth)
)

# Pocket on top opposite side of rib for weight reduction
pocket_x = -arm_length / 4
pocket_y = -arm_width / 4
result = (
    result.faces("+Z")
    .workplane()
    .center(pocket_x, pocket_y)
    .rect(pocket_width, pocket_length)
    .cutBlind(-pocket_depth)
)
