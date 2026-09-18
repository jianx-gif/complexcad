import cadquery as cq

# Parameters
arm_length = 80.0
arm_width = 20.0
arm_thickness = 10.0
rib_width = 12.0
rib_height = 6.0
rib_offset = 6.0
hole_diameter = 6.0
cbore_diameter = 10.0
cbore_depth = 3.0
hole_offset_from_end = 20.0
boss_diameter = 10.0
boss_extension = 8.0
overlap = 2.0

# Derived dimensions
hole_center_x = -arm_length/2 + hole_offset_from_end

# Base plate
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)

# Reinforcing rib on top surface
rib = (
    base.faces(">Z").workplane()
    .rect(arm_length - 2 * rib_offset, rib_width)
    .extrude(rib_height)
)

part = base.union(rib)

# Counterbore hole
part = (
    part.faces(">Z").workplane()
    .center(hole_center_x, 0)
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth)
)

# Groove relief cut into rib
part = (
    part.faces(">Z").workplane()
    .center(0, 0)
    .rect(arm_length * 0.3, rib_width * 0.6)
    .cutBlind(-rib_height / 2)
)

# End tab intersecting the +X face with interior overlap
tab = (
    cq.Workplane("YZ")
    .center(0, 0)
    .rect(boss_diameter, boss_diameter)
    .extrude(boss_extension)
    .translate((arm_length/2 - overlap, 0, arm_thickness/2))
)

# Cylindrical reinforcement overlapping the tab
cyl = (
    cq.Workplane("YZ")
    .center(0, 0)
    .circle(boss_diameter / 2)
    .extrude(boss_extension)
    .translate((arm_length/2 - overlap + boss_extension/2, 0, arm_thickness/2))
)

boss = tab.union(cyl)

result = part.union(boss)