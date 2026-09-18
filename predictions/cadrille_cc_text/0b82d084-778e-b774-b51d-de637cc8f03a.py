import cadquery as cq
outer_diameter = 80.0
inner_diameter = 60.0
cap_height = 20.0
tab_width = 10.0
tab_height = 6.0
inner_round_radius = 12.0
snap_groove_width = 2.0
snap_groove_depth = 3.0
snap_groove_offset = 4.0
chamfer_distance = 0.5
rib_height = 4.0
rib_thickness = 2.0
rib_count = 4
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius - snap_groove_width
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, cap_height - tab_height)
    .lineTo(inner_radius + tab_width, cap_height - tab_height)
    .lineTo(inner_radius + tab_width, cap_height)
    .lineTo(inner_radius, cap_height)
    .close()
)
solid = profile.revolve()
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
tab = (
    cq.Workplane("XY")
    .center(inner_radius + tab_width / 2.0, 0)
    .rect(tab_width, tab_height)
    .extrude(tab_height)
)
solid = solid.cut(tab)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
