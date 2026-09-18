import cadquery as cq
arm_length = 80.0
arm_width = 20.0
arm_thickness = 10.0
rib_height = 6.0
rib_width = 12.0
rib_offset = 20.0
hole_diameter = 6.0
cbore_diameter = 10.0
cbore_depth = 3.0
hole_offset_from_end = 20.0
boss_diameter = 10.0
boss_depth = arm_thickness - 2.0
base = (
    cq.Workplane("XY")
    .rect(arm_width, arm_length)
    .extrude(arm_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, arm_length)
    .extrude(rib_height)
    .translate((0, 0, arm_thickness))
)
base = base.union(rib)
base = base.edges("|Z").chamfer(rib_width)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth)
)
base = base.faces(">Z").workplane().center(0, 0).cskHole(hole_diameter, cbore_diameter, cbore_depth)
result = base
