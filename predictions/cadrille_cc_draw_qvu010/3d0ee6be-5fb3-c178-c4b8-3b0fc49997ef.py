import cadquery as cq
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 50.0
rib_height = 12.0
rib_width = 6.0
rib_thickness = 4.0
rib_count = 8
chamfer_size = 1.0
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_diameter/2, 0)
    .lineTo(outer_diameter/2, thickness)
    .lineTo(outer_diameter/2, thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness)
    .lineTo(outer_diameter/2, thickness + thickness)
    .close()
)
result = profile.revolve()
