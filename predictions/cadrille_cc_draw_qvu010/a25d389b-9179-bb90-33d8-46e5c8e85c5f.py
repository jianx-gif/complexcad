import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
wall_thickness = 5.0
rib_height = 12.0
rib_width = 6.0
rib_thickness = 2.0
rib_count = 8
chamfer_size = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(outer_diameter)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
rib = (
    cq.Workplane('XY')
    .center(inner_radius + rib_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = rib.translate((inner_radius + rib_thickness / 2.0, 0, 0))
combined = outer_cyl.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().center(0, 0).hole(inner_diameter)
combined = combined.faces('>Z').workplane().center(0, 0).hole(inner_diameter)
rib = (
    combined.faces('>Z')
    .workplane()
    .center(inner_radius + rib_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
combined = combined.union(rib)
result = combined
