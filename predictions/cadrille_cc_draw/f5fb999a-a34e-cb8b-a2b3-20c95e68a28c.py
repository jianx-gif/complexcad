import cadquery as cq
outer_radius = 15.0
inner_radius = 20.0
wall_thickness = 2.0
rib_height = 5.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_count = 4
rib_radius = outer_radius - wall_thickness
rib_height = wall_thickness - rib_height
chamfer_size = 0.5
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
