import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
rib_height = 5.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_radius)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(rib_height)
)
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
combined = base.union(rib)
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
result = combined
