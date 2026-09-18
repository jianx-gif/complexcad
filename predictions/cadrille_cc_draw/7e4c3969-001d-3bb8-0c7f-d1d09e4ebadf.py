import cadquery as cq
outer_diameter = 60.0
inner_diameter = 40.0
thickness = 5.0
rib_height = 3.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 8
rib_count = 6
rib_count = 8
rib_radius = outer_diameter/2 - rib_width/2 - 10.0
chamfer_size = 0.5
outer_radius = outer_diameter/2
inner_radius = inner_diameter/2
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
rib = rib.translate((rib_radius, 0, 0))
rib = rib.translate((rib_radius, 0, 0))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
result = combined
