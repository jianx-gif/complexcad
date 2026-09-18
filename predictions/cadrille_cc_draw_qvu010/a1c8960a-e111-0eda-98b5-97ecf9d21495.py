import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
chamfer_size = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(thickness)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(thickness)
rib = outer_cyl.union(inner_cyl)
rib = (
    cq.Workplane('XY')
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
combined = outer_cyl.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
rib = (
    cq.Workplane('XY')
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = combined.union(rib)
result = combined
