import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 80.0
rib_height = 40.0
rib_width = 6.0
rib_thickness = 4.0
rib_count = 6
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter/2, 0)
    .lineTo(inner_diameter/2, thickness)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .lineTo(inner_diameter/2, thickness + rib_height)
    .