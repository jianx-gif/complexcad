import cadquery as cq
outer_diameter = 60.0
inner_diameter = 40.0
thickness = 30.0
wall_thickness = 3.0
rib_width = 6.0
rib_height = 2.0
rib_spacing = 12.0
rib_count = 4
chamfer_size = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius - wall_thickness
rib_count = int((inner_radius + rib_spacing) // rib_spacing)
rib_count = int((inner_radius + rib_spacing) // rib_count)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, rib_height)
    .lineTo(inner_radius, rib_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, rib_height)
    .translate((inner_radius + rib_width / 2.0, 0, rib_count))
)
solid = solid.union(rib)
solid = solid.edges().chamfer(chamfer_size)
solid = (
    solid.faces(">Z")
    .workplane()
    .center(inner_radius + rib_width / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
solid = solid.cut(rib)
solid = solid.edges("|Z").chamfer(chamfer_size)
result = solid
