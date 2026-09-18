import cadquery as cq
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
outer_height = 70.0
wall_thickness = 2.0
boss_radius = 5.0
boss_height = 10.0
boss_offset = 15.0
chamfer_size = 0.5
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, outer_height)
    .lineTo(outer_radius, outer_height + wall_thickness)
    .lineTo(outer_radius + wall_thickness, outer_height + wall_thickness)
    .lineTo(outer_radius + wall_thickness, outer_height + wall_thickness)
    .lineTo(outer_radius, outer_height + wall_thickness)
    .lineTo(outer_radius, outer_height + wall_thickness)
    .lineTo(outer_radius, outer_height + wall_thickness)
    .lineTo(outer_radius, outer_height + wall_thickness)
    .lineTo(outer_radius, outer_height + wall_thickness)
    .lineTo(0, outer_height + wall_thickness)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_height)
    .translate((0, 0, wall_thickness))
)
solid = solid.cut(boss)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
