import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
rib_thickness = 2.0
rib_height = 12.0
rib_spacing = 10.0
chamfer_size = 0.5
outer = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius)
inner = inner.faces('>Z').workplane().hole(inner_radius)
rib = (
    cq.Workplane('XY')
    .center(inner_radius + rib_thickness/2, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((inner_radius + rib_thickness/2, 0, 0))
rib = rib.translate((inner_radius + rib_thickness/2, 0, 0))
rib = rib.translate((inner_radius + rib_thickness/2, 0, 0))
combined = outer.union(rib)
combined = combined.edges('>Z').chamfer(chamfer_size)
result = combined
