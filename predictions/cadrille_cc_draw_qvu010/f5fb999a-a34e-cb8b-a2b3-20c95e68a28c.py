import cadquery as cq
outer_radius = 25.0
inner_radius = 12.0
wall_thickness = 2.0
rib_height = 5.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_distance = 0.5
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_radius)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_radius)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_radius)
)
rib = rib.translate((0, 0, outer_radius - rib_height))
rib = rib.translate((0, 0, outer_radius - rib_height))
rib = rib.translate((0, 0, outer_radius - rib_height))
rib = rib.translate((0, 0, outer_radius - rib_height))
rib = rib.translate((0, 0, outer_radius - rib_height))
rib = rib.translate((0, 0, outer_radius - rib_height))
rib = rib.translate((0, 0, outer_radius - rib_height))
rib = rib.translate((0, 0, outer_radius - rib_height))
rib = rib.translate((0, 0, outer_radius - rib_height))
rib = rib.translate((0, 0, outer_radius - rib_height))
rib = rib.translate((0, 0, outer_radius - rib_height))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_distance)
result = combined
