import cadquery as cq
outer_length = 80.0
outer_width = 50.0
outer_height = 30.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 12.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(outer_length, outer_width)
    .extrude(outer_height)
)
rib = (
    cq.Workplane("XY")
    .rect(outer_length - 2 * wall_thickness, outer_width - 2 * wall_thickness)
    .extrude(outer_height)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_width)
combined = combined.faces(">Z").workplane().center(0, 0).rect(rib_width, outer_width - 2 * wall_thickness).cutBlind(-rib_height)
result = combined
