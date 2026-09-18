import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 10.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
chamfer_distance = 0.5
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
rib_count = 6
rib_radius = outer_diameter / 2.0
rib_count = 4
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_diameter / 2.0, 0)
    .lineTo(outer_diameter / 2.0, thickness)
    .lineTo(outer_diameter / 2.0 + rib_thickness, thickness)
    .lineTo(outer_diameter / 2.0 + rib_thickness, thickness + rib_height)
    .lineTo(0, thickness + rib_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.edges().chamfer(chamfer_distance)
result = solid
