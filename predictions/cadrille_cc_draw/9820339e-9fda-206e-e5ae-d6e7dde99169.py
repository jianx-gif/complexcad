import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
thickness = 20.0
rib_height = 5.0
rib_width = 4.0
rib_thickness = 2.0
rib_offset = 5.0
chamfer_size = 0.5
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
rib_count = 6
rib_count = 4
rib_offset = 15.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, thickness)
    .lineTo(inner_radius, thickness)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve(360)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
solid = solid.union(rib)
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = (
    solid.faces(">Z")
    .workplane()
    .polarArray(radius=outer_radius - rib_offset, startAngle=0, count=rib_count, angle=360)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
solid = solid.union(rib)
solid = solid.edges("|Z").chamfer(chamfer_size)
result = solid
