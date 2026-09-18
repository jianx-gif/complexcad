import cadquery as cq
outer_diameter = 70.0
inner_diameter = 30.0
thickness = 30.0
wall_thickness = 5.0
rib_width = 12.0
rib_height = 10.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_radius = outer_diameter / 2.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius - wall_thickness
rib_count = int(inner_radius + rib_spacing)
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(outer_radius)
combined = combined.faces(">Z").edges().chamfer(outer_radius)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_width)
combined = combined.faces(">Z").workplane().rect(inner_radius, inner_radius).cutBlind(-inner_radius)
result = combined
