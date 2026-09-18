import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
wall_thickness = 8.0
rib_height = 40.0
rib_width = 12.0
rib_thickness = 4.0
rib_count = 6
chamfer_size = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(outer_diameter)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(inner_cyl)
rib = (
    cq.Workplane('XY')
    .center(outer_radius - rib_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = rib.translate((outer_radius - rib_thickness / 2.0, 0, 0))
combined = outer_cyl.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
combined = combined.faces('>Z').workplane().hole(inner_diameter)
rib = (
    cq.Workplane('XY')
    .box(rib_width, rib_height, rib_thickness)
    .translate((outer_radius - rib_thickness / 2.0, 0, 0))
)
combined = combined.union(rib)
result = combined
