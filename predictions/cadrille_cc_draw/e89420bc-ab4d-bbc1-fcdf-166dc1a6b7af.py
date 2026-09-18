import cadquery as cq
outer_length = 80.0
outer_width = 40.0
outer_height = 30.0
wall_thickness = 5.0
rib_width = 10.0
rib_height = 15.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_spacing = 12.0
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
rib = (
    cq.Workplane("XY")
    .rect(outer_length - 2 * wall_thickness, outer_width - 2 * wall_thickness)
    .extrude(outer_height)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).rect(rib_width, outer_width - 2 * wall_thickness).cutBlind(-wall_thickness)
combined = combined.faces(">Z").workplane().center(0, 0).rect(rib_width, outer_width - 2 * wall_thickness).extrude(rib_height)
combined = combined.union(rib)
result = combined
