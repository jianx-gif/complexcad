import cadquery as cq
outer_radius = 80.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
wall_thickness = 2.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 15.0
fillet_radius = 2.0
chamfer_distance = 1.0
mount_hole_dia = 4.0
mount_hole_spacing = 30.0
mount_hole_offset = 15.0
base = (
    cq.Workplane("XY")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness + rib_height)
    .lineTo(inner_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .lineTo(outer_radius, wall_thickness + rib_height)
    .close()
    .extrude(wall_thickness)
)
result = base
