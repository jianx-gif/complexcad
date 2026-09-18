import cadquery as cq
outer_radius = 40.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
rib_thickness = 2.0
rib_height = 12.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
rib_count = 6
rib_count = 8
rib_offset = 10.0
chamfer_size = 0.5
outer = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_radius)
)
inner = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(outer_radius)
)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(rib_height)
)
rib = rib.translate((inner_radius + rib_thickness/2, 0, 0))
rib = rib.translate((inner_radius + rib_thickness/2, 0, 0))
combined = outer.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
result = combined
