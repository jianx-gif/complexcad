import cadquery as cq
outer_diameter = 80.0
inner_diameter = 40.0
thickness = 10.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
rib_radius = inner_diameter / 2.0
chamfer_size = 0.5
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
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().polarArray(radius=inner_radius, count=rib_count, startAngle=0, angle=360).hole(inner_diameter)
result = combined
