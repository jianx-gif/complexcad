import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 3.0
rib_height = 10.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
rib_count = 6
rib_count = 4
rib_spacing = 15.0
chamfer_size = 1.0
outer = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius)
rib = (
    cq.Workplane('XY')
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((outer_radius - rib_width/2, 0, 0))
)
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
combined = outer.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
result = combined
