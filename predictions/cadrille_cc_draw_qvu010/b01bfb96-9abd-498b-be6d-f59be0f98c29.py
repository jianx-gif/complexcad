import cadquery as cq
outer_diameter = 70.0
inner_diameter = 30.0
wall_thickness = 4.0
inner_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
fillet_radius = 2.0
chamfer_distance = 1.0
mount_hole_diameter = 4.0
mount_hole_radius = outer_diameter / 2.0
mount_hole_count = 6
mount_hole_radius = mount_hole_radius - wall_thickness
outer_radius = outer_diameter / 2.0
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, inner_radius)
    .lineTo(inner_radius + wall_thickness, inner_radius)
    .lineTo(inner_radius + wall_thickness, inner_radius + wall_thickness)
    .lineTo(inner_radius + wall_thickness, inner_radius + wall_thickness)
    .lineTo(inner_radius, inner_radius)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(fillet_radius)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
mount_hole = (
    cq.Workplane("XY")
    .circle(mount_hole_radius)
    .extrude(mount_hole_count)
)
solid = solid.cut(mount_hole)
solid = solid.edges().chamfer(chamfer_distance)
result = solid
