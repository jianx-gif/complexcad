import cadquery as cq
outer_diameter = 70.0
inner_diameter = 30.0
thickness = 20.0
rib_height = 5.0
rib_width = 6.0
rib_thickness = 4.0
rib_count = 6
chamfer_size = 1.0
mount_hole_diameter = 4.0
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
    .line