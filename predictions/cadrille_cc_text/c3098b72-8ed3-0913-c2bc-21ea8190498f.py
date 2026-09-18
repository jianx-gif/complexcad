import cadquery as cq
outer_diameter = 80.0
wall_thickness = 3.0
cap_height = 20.0
snap_width = 5.0
snap_depth = 4.0
groove_width = 2.0
groove_depth = 1.0
chamfer_size = 0.5
groove_outer_radius = outer_diameter / 2.0
inner_radius = outer_diameter / 2.0
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, cap_height - snap_depth)
    .lineTo(inner_radius + snap_width, cap_height - snap_depth)
    .lineTo(inner_radius + snap_width, cap_height)
    .lineTo(inner_radius, cap_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
groove = (
    cq.Workplane("XY")
    .circle(groove_outer_radius)
    .extrude(groove_depth)
    .translate((0, 0, wall_thickness))
)
solid = solid.cut(groove)
solid = solid.edges().chamfer(chamfer_size)
result = solid
