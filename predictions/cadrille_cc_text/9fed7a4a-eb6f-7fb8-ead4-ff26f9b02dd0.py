import cadquery as cq
outer_radius = 45.0
inner_radius = 30.0
block_height = 70.0
rib_thickness = 4.0
rib_height = 55.0
fillet_radius = 5.0
blind_hole_diameter = 12.0
blind_hole_depth = 25.0
chamfer_size = 1.5
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, block_height)
    .lineTo(outer_radius, block_height)
    .lineTo(outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_thickness/2, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.edges().chamfer(chamfer_size)
result = solid
