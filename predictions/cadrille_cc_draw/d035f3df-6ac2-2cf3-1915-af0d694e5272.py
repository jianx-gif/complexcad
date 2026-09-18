import cadquery as cq
outer_radius = 20.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
wall_thickness = wall_thickness
rib_height = 2.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 6
chamfer_size = 0.5
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
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(wall_thickness)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
result = combined
