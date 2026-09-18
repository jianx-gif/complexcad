import cadquery as cq
outer_radius = 20.0
inner_radius = 15.0
wall_thickness = 1.0
rib_height = 6.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_distance = 0.5
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_radius)
)
rib = (
    cq.Workplane("XY")
    .center(inner_radius, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((inner_radius, 0, 0))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_distance)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().center(inner_radius - rib_width/2, 0).rect(rib_width, rib_height).cutBlind(-rib_height)
combined = combined.faces(">Z").workplane().center(inner_radius - rib_width/2, 0).rect(rib_width, rib_height).cutBlind(-rib_height)
result = combined
