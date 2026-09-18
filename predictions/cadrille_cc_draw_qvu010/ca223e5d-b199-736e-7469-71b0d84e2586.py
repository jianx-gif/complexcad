import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 2.0
inner_radius = inner_radius - wall_thickness
rib_height = 5.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 6
chamfer_distance = 0.5
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
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_distance)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, rib_height)
    .translate((inner_radius - rib_width / 2, 0, 0))
)
combined = combined.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_distance)
result = combined
