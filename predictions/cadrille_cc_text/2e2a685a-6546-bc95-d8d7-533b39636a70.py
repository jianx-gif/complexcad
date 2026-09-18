import cadquery as cq
bracket_length = 80.0
bracket_width = 40.0
bracket_base_thickness = 6.0
flange_step_length = 50.0
flange_step_width = 30.0
flange_step_height = 4.0
corner_fillet_radius = 1.0
blind_hole_diameter = 5.0
blind_hole_depth = 8.0
mount_hole_diameter = 4.0
mount_hole_spacing = 25.0
mount_hole_offset = 10.0
rib_width = 6.0
rib_height = 10.0
rib_spacing = 20.0
chamfer_distance = 1.0
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_base_thickness)
)
flange = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(flange_step_length, flange_step_width)
    .extrude(flange_step_height)
)
flange = (
    flange.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(blind_hole_diameter, blind_hole_depth)
)
rib = (
    flange.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_spacing)
)
result = base.union(rib)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(blind_hole_diameter, blind_hole_depth)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(mount_hole_diameter, blind_hole_depth)
)
result = result.edges("|Z").fillet(corner_fillet_radius)
