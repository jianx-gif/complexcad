import cadquery as cq
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
base_thickness = 5.0
rib_height = 4.0
rib_width = 10.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, base_thickness)
    .lineTo(outer_radius, base_thickness + rib_height)
    .lineTo(outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_thickness/2, 0)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
