import cadquery as cq
outer_diameter = 70.0
inner_diameter = 30.0
thickness = 20.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
rib_count = 6
chamfer_size = 1.0
mount_hole_dia = 4.0
mount_hole_spacing = 30.0
rib_count = 4
rib_radius = outer_diameter / 2.0
rib_count = 4
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2.0, 0)
    .lineTo(inner_diameter / 2.0, rib_height)
    .lineTo(outer_diameter / 2.0, rib_height)
    .lineTo(outer_diameter / 2.0, rib_height + rib_width)
    .lineTo(inner_diameter / 2.0, rib_height + rib_width)
    .lineTo(inner_diameter / 2.0, rib_height + rib_width)
    .lineTo(inner_diameter / 2.0, rib_height + rib_width)
    .lineTo(inner_diameter / 2.0, rib_height + rib_width)
    .lineTo(inner_diameter / 2.0, 0)
    .close()
)
result = (
    profile
    .revolve()
    .shell(-thickness)
    .edges()
    .chamfer(chamfer_size)
    .faces(">Z")
    .workplane()
    .hole(mount_hole_dia)
    .faces(">Z")
    .workplane()
    .hole(mount_hole_dia)
)
