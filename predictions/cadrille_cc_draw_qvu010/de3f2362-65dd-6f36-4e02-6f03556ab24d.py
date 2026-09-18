import cadquery as cq
outer_radius = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
rib_thickness = 2.0
rib_height = 12.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
rib_spacing = 12.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(outer_radius, outer_radius)
    .extrude(outer_radius)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_thickness, rib_height)
    .extrude(rib_thickness)
    .translate((0, 0, wall_thickness))
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
result = combined
