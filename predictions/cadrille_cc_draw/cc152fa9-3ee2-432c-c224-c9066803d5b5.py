import cadquery as cq
outer_radius = 30.0
wall_thickness = 10.0
inner_radius = outer_radius - wall_thickness
base_thickness = 12.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 15.0
rib_count = 8
chamfer_size = 0.5
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(rib_height)
)
rib = rib.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
result = combined
