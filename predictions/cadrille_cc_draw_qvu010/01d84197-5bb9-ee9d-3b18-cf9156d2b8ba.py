import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 30.0
rib_height = 5.0
rib_width = 10.0
rib_thickness = 2.0
rib_count = 6
chamfer_size = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius - inner_radius
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
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().polarArray(radius=outer_radius - rib_thickness/2, count=rib_count, startAngle=0, angle=360).hole(rib_thickness)
result = combined
