import cadquery as cq
import cadquery as cq
arm_length = 80.0
arm_width = 30.0
arm_thickness = 6.0
rib_height = 2.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 8
rib_count = 6
rib_margin = 5.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(arm_length, 0)
    .lineTo(arm_length, arm_width)
    .lineTo(arm_length, arm_thickness)
    .lineTo(0, arm_thickness)
    .close()
    .revolve()
)
rib = (
    base.faces(">Z")
    .workplane()
    .center(0, arm_thickness/2)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = rib.edges(">Z").chamfer(chamfer_size)
rib = (
    rib.faces(">Z")
    .workplane()
    .center(0, arm_thickness/2)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = rib
