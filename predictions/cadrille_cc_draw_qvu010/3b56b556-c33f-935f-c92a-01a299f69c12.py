import cadquery as cq
outer_length = 80.0
outer_width = 50.0
outer_height = 20.0
wall_thickness = 1.5
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 6
rib_spacing = 12.0
rib_offset = 5.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(outer_length, outer_width)
    .extrude(outer_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, outer_height)
    .extrude(rib_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, outer_height)
    .extrude(rib_height)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.faces(">Z").workplane().rect(rib_width, outer_height).extrude(rib_height)
combined = combined.faces(">Z").workplane().rect(rib_width, outer_height).cutBlind(-rib_height)
combined = combined.faces(">Z").workplane().rect(rib_width, outer_height).cutBlind(-rib_height)
result = combined
