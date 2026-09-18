import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 1.0
mount_hole_dia = 4.0
mount_hole_offset = 10.0
rib_count = 4
rib_count = 6
rib_count = 4
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter/2, 0)
    .lineTo(outer_diameter/2, 0)
    .lineTo(outer_diameter/2, thickness)
    .lineTo(outer_diameter/2, thickness + rib_height)
    .lineTo(outer_diameter/2, thickness + rib_height)
    .lineTo(outer_diameter/2, thickness + rib_height)
    .lineTo(outer_diameter/2, 0)
    .close()
)
result = (
    profile
    .revolve()
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
    .faces(">Z")
    .workplane()
    .hole(mount_hole_dia)
    .faces(">Z")
    .workplane()
    .hole(mount_hole_dia)
)
