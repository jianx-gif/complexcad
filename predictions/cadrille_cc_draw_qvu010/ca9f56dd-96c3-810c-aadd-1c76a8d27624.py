import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 35.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_radius = inner_diameter / 2.0
rib_height = thickness / 2.0
rib_spacing = 10.0
chamfer_size = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
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
    .circle(outer_radius)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness / 2.0))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().polarArray(radius=inner_radius - rib_spacing/2, count=rib_count, startAngle=0, angle=360).hole(rib_radius)
result = combined
