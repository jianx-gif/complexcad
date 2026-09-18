import cadquery as cq
outer_diameter = 80.0
plate_thickness = 8.0
inner_diameter = 30.0
pocket_outer_radius = 12.0
pocket_inner_radius = 6.0
pocket_depth = 4.0
chamfer_distance = 2.0
mount_hole_dia = 6.0
mount_hole_offset = 25.0
rib_width = 3.0
rib_angle = 30.0
rib_height = plate_thickness - 2 * pocket_outer_radius
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius - pocket_outer_radius
pocket = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, plate_thickness)
    .lineTo(outer_radius, plate_thickness)
    .lineTo(outer_radius, 0)
    .close()
)
pocket = (
    cq.Workplane("XY")
    .circle(pocket_outer_radius)
    .circle(pocket_inner_radius)
    .extrude(pocket_depth)
)
pocket = pocket.cut(pocket)
mount_hole = (
    cq.Workplane("XY")
    .circle(mount_hole_dia / 2.0)
    .extrude(pocket_depth)
)
mount_hole = (
    cq.Workplane("XY")
    .circle(mount_hole_dia / 2.0)
    .extrude(pocket_depth)
)
mount_hole = (
    mount_hole
    .faces(">Z")
    .workplane()
    .polarArray(radius=mount_hole_offset, startAngle=0, angle=360, count=mount_hole)
    .hole(mount_hole_dia)
)
result = mount_hole
