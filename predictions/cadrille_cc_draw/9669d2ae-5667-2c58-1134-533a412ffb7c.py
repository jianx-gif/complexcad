import cadquery as cq
outer_radius = 85.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
rib_thickness = 5.0
rib_height = 30.0
rib_offset = 10.0
rib_count = 6
rib_count = 4
rib_spacing = 12.0
chamfer_size = 0.5
rib_count = 4
rib_spacing = 12.0
rib_height = 20.0
rib_offset = outer_radius - rib_thickness/2
base = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, rib_offset)
    .lineTo(inner_radius, rib_offset)
    .lineTo(inner_radius, rib_height)
    .lineTo(inner_radius, rib_height)
    .lineTo(outer_radius, rib_height)
    .lineTo(outer_radius, rib_height)
    .lineTo(outer_radius, rib_height)
    .lineTo(outer_radius, rib_height)
    .lineTo(outer_radius, rib_height)
    .lineTo(outer_radius, rib_height)
    .lineTo(outer_radius, rib_height)
    .lineTo(outer_radius, rib_height)
    .lineTo(0, rib_height)
    .close()
    .revolve()
)
rib = (
    cq.Workplane("XY")
    .center(0, rib_offset)
    .rect(rib_thickness, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, rib_height - rib_height/2))
rib = rib.translate((0, 0, rib_height - rib_height/2))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
result = combined
