import cadquery as cq
outer_diameter = 50.0
inner_diameter = 30.0
wall_thickness = 2.0
rib_height = 4.0
rib_width = 6.0
rib_depth = 2.0
chamfer_distance = 0.5
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
rib_count = 6
rib_radius = outer_diameter / 2.0
rib_height = wall_thickness + rib_height
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2.0, 0)
    .lineTo(inner_diameter / 2.0, rib_height)
    .lineTo(outer_diameter / 2.0, rib_height)
    .lineTo(outer_diameter / 2.0, rib_height)
    .lineTo(outer_diameter / 2.0, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2.0, rib_height / 2.0)
    .rect(rib_width, rib_height)
    .extrude(rib_depth)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
