import cadquery as cq
outer_radius = 40.0
hub_radius = 15.0
thickness = 30.0
hub_radius = hub_radius + 2.0
groove_depth = 8.0
groove_width = 12.0
fillet_radius = 1.0
countersink_base_radius = 3.0
countersink_base_radius = 2.0
countersink_base_radius = 2.0
mount_hole_radius = 1.5
mount_hole_count = 4
mount_hole_radius = 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, thickness)
    .lineTo(hub_radius, thickness)
    .lineTo(hub_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(fillet_radius)
groove = (
    cq.Workplane("XY")
    .circle(groove_depth)
    .extrude(groove_width)
    .translate((0, 0, thickness))
)
solid = solid.cut(groove)
solid = solid.edges().fillet(fillet_radius)
solid = solid.faces(">Z").workplane().hole(countersink_base_radius * 2)
mount_hole = (
    cq.Workplane("XY")
    .polarArray(radius=mount_hole_radius, count=mount_hole_count, startAngle=0, angle=360)
    .hole(mount_hole_radius * 2)
)
solid = solid.cut(mount_hole)
solid = solid.edges().fillet(fillet_radius)
result = solid
