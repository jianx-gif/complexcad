import cadquery as cq
outer_radius = 20.0
inner_radius = 15.0
wall_thickness = 2.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 12
chamfer_distance = 0.5
outer = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(inner_radius)
rib = (
    cq.Workplane('XY')
    .circle(inner_radius)
    .extrude(rib_height)
    .translate((outer_radius - rib_width/2, 0, wall_thickness))
)
rib = rib.translate((outer_radius - rib_width/2, 0, wall_thickness))
combined = outer.union(rib)
combined = combined.edges().chamfer(chamfer_distance)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
combined = combined.faces('>Z').workplane().hole(inner_radius * 2)
result = combined
