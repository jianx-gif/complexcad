import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 60.0
rib_height = 12.0
rib_width = 10.0
rib_depth = 8.0
rib_count = 6
rib_spacing = 12.0
rib_count = 4
rib_radius = outer_diameter / 2.0
rib_count = 6
rib_spacing = 15.0
rib_count = 4
rib_radius = inner_diameter / 2.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
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
rib = rib.translate((0, 0, rib_height))
rib = rib.translate((0, 0, rib_height))
rib = rib.translate((0, 0, rib_height))
combined = base.union(rib)
combined = combined.edges().chamfer(outer_radius)
combined = combined.faces(">Z").workplane().hole(rib_radius * 2)
combined = combined.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_depth)
combined = combined.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_depth)
combined = combined.union(rib)
combined = combined.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_depth)
result = combined
