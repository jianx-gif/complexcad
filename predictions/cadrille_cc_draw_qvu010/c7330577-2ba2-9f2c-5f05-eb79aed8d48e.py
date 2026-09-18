import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
chamfer_size = 0.5
outer = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius)
inner = inner.faces('>Z').workplane().hole(inner_radius)
rib = (
    cq.Workplane('XY')
    .box(rib_width, rib_height, rib_width)
    .translate((inner_radius - rib_width/2, 0, 0))
)
rib = rib.translate((inner_radius - rib_width/2, 0, 0))
rib = rib.translate((inner_radius - rib_width/2, 0, 0))
combined = outer.union(rib)
combined = combined.edges('>Z').chamfer(chamfer_size)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
result = combined
