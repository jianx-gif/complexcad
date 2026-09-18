import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
wall_thickness = 5.0
rib_height = 20.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_radius = outer_diameter / 2.0
rib_height = wall_thickness * 0.6
rib_count = 4
rib_count = 6
rib_radius = outer_diameter / 2.0
rib_count = 4
rib_radius = outer_diameter / 2.0
rib_count = 3
rib_radius = rib_radius + rib_height / 2.0
rib_count = int((inner_diameter / 2.0) / rib_count)
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(rib_height)
)
rib = (
    cq.Workplane("XY")
    .circle(rib_radius)
    .extrude(rib_height)
)
rib = rib.translate((rib_radius, 0, rib_height / 2.0))
)
rib = rib.translate((rib_radius, 0, rib_height / 2.0))
combined = base.union(rib)
combined = combined.edges().chamfer(outer_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
result = combined
