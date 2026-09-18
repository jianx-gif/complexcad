import cadquery as cq
outer_diameter = 60.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
fillet_radius = 2.0
chamfer_distance = 1.0
mount_hole_dia = 4.0
mount_hole_radius = outer_diameter / 2.0
mount_hole_count = 4
mount_hole_radius = inner_radius + wall_thickness
outer_radius = outer_diameter / 2.0
inner_radius = inner_radius + wall_thickness
inner_radius = inner_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, inner_radius)
    .lineTo(inner_radius, inner_radius + wall_thickness)
    .lineTo(inner_radius, inner_radius + wall_thickness)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(fillet_radius)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(mount_hole_dia)
solid = (
    solid.faces(">Z").workplane()
    .polarArray(radius=mount_hole_radius, startAngle=0, angle=360, count=mount_hole_count)
    .hole(mount_hole_dia)
)
result = solid
