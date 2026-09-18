import cadquery as cq
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 10.0
wall_thickness = 2.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
chamfer_size = 0.5
mount_hole_dia = 4.0
mount_hole_spacing = 20.0
rib_count = int(360 / rib_spacing)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2, 0)
    .lineTo(outer_diameter / 2, 0)
    .lineTo(outer_diameter / 2, thickness)
    .lineTo(outer_diameter / 2, thickness)
    .lineTo(outer_diameter / 2, 0)
    .close()
)
solid = profile.revolve(360)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, rib_width)
    .translate((outer_diameter / 2 - rib_height / 2, 0, wall_thickness))
)
rib = rib.translate((outer_diameter / 2 - rib_width / 2, 0, wall_thickness))
result = solid.union(rib)
result = result.faces(">Z").edges().chamfer(chamfer_size)
