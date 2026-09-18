import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 15.0
rib_height = 10.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 1.0
mount_hole_dia = 5.0
mount_hole_spacing = 30.0
rib_count = 4
rib_radius = outer_diameter / 2.0
rib_count = 3
rib_count = 4
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2.0, 0)
    .lineTo(outer_diameter / 2.0, 0)
    .lineTo(outer_diameter / 2.0, thickness)
    .lineTo(outer_diameter / 2.0,  thickness)
    .lineTo(outer_diameter / 2.0, 0)
    .close()
)
result = profile.revolve()
result = result.faces(">Z").edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = result.union(rib)
result = result.edges("|Z").chamfer(chamfer_size)
result = result.faces(">Z").workplane().hole(mount_hole_dia)
result = result.faces(">Z").workplane().hole(mount_hole_dia)
result = result.faces(">Z").workplane().hole(mount_hole_dia)
