import cadquery as cq

outer_diameter = 80.0
inner_diameter = 30.0
collar_length = 30.0
groove_width = 10.0
groove_depth = 8.0
fillet_radius = 1.0
chamfer_distance = 0.5
set_screw_diameter = 5.0
set_screw_head_diameter = 9.0
set_screw_head_depth = 2.0
set_screw_offset = 12.0

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
groove_start = (collar_length - groove_width) / 2.0
groove_end = groove_start + groove_width

profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, groove_start)
    .lineTo(outer_radius - groove_depth, groove_start)
    .lineTo(outer_radius - groove_depth, groove_end)
    .lineTo(outer_radius, groove_end)
    .lineTo(outer_radius, collar_length)
    .lineTo(inner_radius, collar_length)
    .lineTo(inner_radius, 0)
    .close()
)

solid = profile.revolve()

solid = solid.faces(">Z").edges().fillet(fillet_radius)

solid = solid.edges().chamfer(chamfer_distance)

solid = (
    solid.faces(">Z")
    .workplane()
    .center(set_screw_offset, 0)
    .cskHole(set_screw_diameter, set_screw_head_diameter, set_screw_head_depth)
)

result = solid