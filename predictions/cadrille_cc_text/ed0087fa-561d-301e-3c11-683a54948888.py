import cadquery as cq
outer_radius = 45.0
height = 30.0
wall_thickness = 5.0
shaft_radius = 15.0
bearing_pocket_radius = 8.0
bearing_pocket_depth = 6.0
blind_hole_radius = 5.0
blind_hole_depth = 12.0
blind_hole_count = 6
blind_hole_radius = 12.0
chamfer_size = 1.5
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(outer_radius + wall_thickness, height)
    .lineTo(outer_radius + wall_thickness, height - bearing_pocket_depth)
    .lineTo(outer_radius, height - bearing_pocket_depth)
    .lineTo(outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
blind_hole = (
    cq.Workplane("XY")
    .circle(blind_hole_radius)
    .extrude(blind_hole_depth)
)
solid = solid.cut(blind_hole)
solid = solid.edges().chamfer(chamfer_size)
result = solid
