import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 60.0
rib_height = 12.0
rib_width = 10.0
rib_thickness = 4.0
rib_count = 6
chamfer_size = 1.0
hole_diameter = 5.0
hole_depth = thickness / 2.0
hole_count = 8
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
    .lineTo(inner_diameter/2, thickness + rib