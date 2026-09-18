import cadquery as cq
outer_radius = 20.0
wall_thickness = 4.0
inner_radius = outer_radius - wall_thickness
wall_thickness = 1.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 15.0
chamfer_distance = 0.5
rib_count = int((inner_radius - wall_thickness) // rib_spacing)
base = (
    cq.Workplane("XY")
    .rect(outer_radius, outer_radius)
    .extrude(wall_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(wall_thickness)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_distance)
result = combined
