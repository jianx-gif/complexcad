import cadquery as cq
arm_length = 80.0
arm_width = 20.0
arm_thickness = 8.0
tab_width = 30.0
tab_height = 12.0
cable_hole_diameter = 4.0
cable_hole_offset = 5.0
chamfer_size = 0.8
mount_hole_diameter = 3.0
mount_hole_offset = 10.0
rib_width = 6.0
rib_height = arm_thickness - 2.0
rib_length = arm_length - 2 * tab_width
rib_count = int((arm_length - 2 * tab_width) // rib_length)
base = (
    cq.Workplane("XY")
    .rect(arm_length, arm_width)
    .extrude(arm_thickness)
)
tab = (
    cq.Workplane("XY")
    .rect(tab_width, tab_height)
    .extrude(tab_thickness)
    .translate((0, 0, arm_thickness))
)
tab = (
    cq.Workplane("XY")
    .rect(tab_width, tab_height)
    .extrude(tab_thickness)
    .translate((0, 0, arm_thickness))
)
tab = tab.union(tab)
tab = (
    tab.faces(">Z")
    .workplane()
    .center(arm_length/2 - mount_hole_offset, 0)
    .hole(mount_hole_diameter)
)
result = base.union(tab)
result = result.edges("|Z").chamfer(chamfer_size)
