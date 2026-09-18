import cadquery as cq
outer_radius = 20.0
inner_radius = 15.0
wall_thickness = 2.0
rib_height = 5.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 6
chamfer_size = 0.5
outer = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius)
rib = (
    cq.Workplane('XY')
    .circle(inner_radius)
    .extrude(rib_height)
    .translate((outer_radius - rib_width/2, 0, 0))
)
rib = rib.translate((outer_radius - rib_width/2, 0, 0))
combined = outer.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces('>Z').edges().chamfer(chamfer_size)
result = combined
