import cadquery as cq
outer_diameter = 80.0
inner_diameter = 40.0
thickness = 50.0
rib_height = 12.0
rib_width = 10.0
rib_depth = 8.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
rib_offset = 15.0
chamfer_size = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
rib_count = int((inner_radius - rib_spacing) // rib_spacing)
rib_base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = rib.translate((rib_offset, 0, 0))
combined = outer_radius.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces("<Z").workplane().hole(inner_diameter)
combined = combined.faces("<Z").workplane().hole(inner_diameter)
combined = combined.faces("<Z").workplane().hole(inner_diameter)
result = combined
