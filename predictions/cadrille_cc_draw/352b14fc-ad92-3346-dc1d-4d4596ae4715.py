import cadquery as cq
outer_radius = 40.0
inner_radius = 30.0
wall_thickness = 2.0
rib_height = 8.0
rib_width = 6.0
rib_thickness = 2.0
rib_count = 8
chamfer_distance = 1.0
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
rib_count = int((inner_radius - rib_height) // rib_count)
base = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, rib_height)
    .lineTo(inner_radius + rib_thickness, rib_height)
    .lineTo(inner_radius + rib_thickness, rib_height + rib_height)
    .lineTo(inner_radius + rib_thickness, rib_height + rib_height)
    .lineTo(inner_radius, rib_height + rib_height)
    .lineTo(inner_radius, rib_height + rib_height)
    .lineTo(inner_radius, rib_height + rib_thickness)
    .lineTo(inner_radius, rib_height + rib_thickness)
    .lineTo(inner_radius, rib_height + rib_thickness)
    .lineTo(inner_radius, rib_height + rib_thickness)
    .lineTo(inner_radius, rib_height + rib_thickness)
    .lineTo(inner_radius, rib_height + rib_thickness)
    .lineTo(inner_radius, rib_height + rib_thickness)
    .lineTo(inner_radius, rib_height + rib_thickness)
    .lineTo(inner_radius, rib_height + rib_thickness)
    .lineTo(inner_radius, rib_height + rib_thickness)
    .lineTo(inner_radius, rib_height + rib_thickness)
    .lineTo(inner_radius, rib_height + rib_thickness)
    .lineTo(inner_radius, rib_height + rib_thickness)
    .lineTo(inner_radius, rib_height + rib_thickness)
    .lineTo(inner_radius, rib_height + rib_thickness)
    .lineTo(inner_radius, rib_height + rib_thickness)
    .close()
)
result = (
    base
    .cut(
        cq.Workplane("XY")
        .circle(outer_radius)
        .extrude(outer_radius * 2)
        .translate((outer_radius - wall_thickness / 2, 0, 0))
    )
    .faces(">Z")
    .workplane()
    .hole(mount_hole_diameter)
    .edges()
    .chamfer(chamfer_distance)
)
