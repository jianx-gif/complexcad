import cadquery as cq
outer_diameter = 100.0
inner_diameter = 30.0
thickness = 15.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 12
rib_count = 8
rib_spacing = 12.0
rib_height = 8.0
rib_offset = 10.0
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
    .center(inner_radius + rib_offset, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_height)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_count)
result = combined
