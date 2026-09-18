import cadquery as cq
outer_radius = 40.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
rib_height = 12.0
rib_width = 2.0
rib_depth = 2.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_radius = outer_radius - wall_thickness
rib_height = 10.0
rib_count = 6
rib_spacing = 12.0
chamfer_distance = 0.5
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_radius)
)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_radius, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((outer_radius - rib_radius, 0, 0))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_distance)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_radius * 2)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_height)
result = combined
