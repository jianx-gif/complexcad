import cadquery as cq
outer_width = 80.0
outer_depth = 40.0
outer_height = 20.0
wall_thickness = 2.0
rib_width = 12.0
rib_height = 10.0
rib_spacing = 12.0
rib_count = 6
chamfer_size = 0.5
outer = (
    cq.Workplane("XY")
    .rect(outer_width, outer_depth)
    .extrude(outer_height)
)
inner = (
    cq.Workplane("XY")
    .rect(outer_width - 2 * wall_thickness, outer_depth - 2 * wall_thickness)
    .extrude(outer_height)
)
rib = (
    cq.Workplane("XY")
    .rect(outer_width - 2 * wall_thickness, outer_depth - 2 * wall_thickness)
    .extrude(outer_height)
)
combined = outer.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_width)
combined = combined.faces(">Z").workplane().center(0, 0).hole(rib_height)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
