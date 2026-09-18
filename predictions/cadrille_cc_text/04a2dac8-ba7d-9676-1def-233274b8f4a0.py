import cadquery as cq
arm_base_radius = 15.0
arm_length = 60.0
arm_thickness = 5.0
flange_width = 10.0
flange_thickness = 5.0
rib_height = 3.0
rib_width = 4.0
blind_hole_diameter = 4.0
blind_hole_depth = 3.5
slot_width = 2 * flange_width
slot_height = 20.0
slot_depth = 10.0
chamfer_size = 0.8
rib_offset_angle = 30.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(arm_base_radius, 0)
    .lineTo(arm_base_radius, arm_length)
    .lineTo(flange_width, arm_length)
    .lineTo(flange_width, arm_length - flange_thickness)
    .lineTo(0, arm_length - flange_thickness)
    .close()
)
solid = profile.revolve(360)
solid = solid.faces(">Z").workplane().hole(blind_hole_diameter, blind_hole_depth)
solid = solid.faces(">Z").workplane().center(0, 0).circle(rib_height).extrude(arm_thickness)
solid = solid.faces(">Z").workplane().center(0, 0).circle(rib_width).extrude(arm_thickness + 0.1)
solid = solid.edges("|Z").chamfer(chamfer_size)
slot = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(slot_width, slot_height)
    .extrude(arm_thickness + 0.1)
)
solid = solid.cut(slot)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
