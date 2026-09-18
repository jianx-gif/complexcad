import cadquery as cq
outer_diameter = 60.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = inner_diameter / 2
rib_width = 8.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
rib_count = 3
chamfer_size = 0.5
outer_radius = outer_diameter / 2
inner_radius = inner_radius + wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_radius)
)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(rib_height)
)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(rib_height)
)
rib = rib.translate((inner_radius + rib_thickness / 2, 0, 0))
)
rib = rib.translate((inner_radius + rib_thickness / 2, 0, 0))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
result = combined
