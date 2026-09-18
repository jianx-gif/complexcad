import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 5.0
rib_height = 12.0
rib_width = 6.0
rib_thickness = 2.0
rib_count = 8
chamfer_size = 0.5
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_radius)
)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(rib_height)
)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
combined = base.union(rib)
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
result = combined
