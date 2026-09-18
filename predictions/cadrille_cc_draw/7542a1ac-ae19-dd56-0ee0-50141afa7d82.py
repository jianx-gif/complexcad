import cadquery as cq
outer_radius = 15.0
inner_radius = 15.0
thickness = 4.0
rib_thickness = 2.0
rib_height = 3.0
rib_count = 8
chamfer_distance = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, thickness)
    .lineTo(outer_radius, thickness)
    .lineTo(outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_thickness / 2, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_thickness)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
