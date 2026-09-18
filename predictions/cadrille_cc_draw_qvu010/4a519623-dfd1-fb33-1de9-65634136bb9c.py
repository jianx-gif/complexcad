import cadquery as cq
outer_width = 80.0
outer_height = 60.0
outer_height = 60.0
wall_thickness = 5.0
rib_width = 12.0
rib_height = 10.0
rib_spacing = 15.0
rib_count = 6
rib_count = 4
chamfer_size = 1.0
outer = (
    cq.Workplane("XY")
    .rect(outer_width, outer_height)
    .extrude(outer_height)
)
inner = (
    cq.Workplane("XY")
    .rect(outer_width - 2 * wall_thickness, outer_height - 2 * wall_thickness)
    .extrude(outer_height)
)
rib = (
    cq.Workplane("XY")
    .rect(outer_width - 2 * wall_thickness, outer_height - 2 * wall_thickness)
    .extrude(outer_height)
)
combined = outer.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.faces(">Z").workplane().rect(rib_width, outer_height).extrude(rib_height)
combined = combined.faces(">Z").workplane().rect(rib_width, outer_height).cutBlind(-rib_height)
result = combined
