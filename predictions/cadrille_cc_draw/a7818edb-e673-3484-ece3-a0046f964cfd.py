import cadquery as cq
outer_width = 70.0
outer_height = 80.0
outer_height = 20.0
wall_thickness = 5.0
rib_width = 10.0
rib_height = 12.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(outer_width, outer_height)
    .extrude(outer_height)
)
rib = (
    cq.Workplane("XY")
    .rect(outer_width - 2 * wall_thickness, outer_height - 2 * wall_thickness)
    .extrude(outer_height)
)
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, outer_height - 2 * wall_thickness)
    .cutBlind(-outer_height)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, outer_height - 2 * wall_thickness)
    .extrude(outer_height)
)
combined = combined.union(rib)
result = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, outer_height - 2 * wall_thickness)
    .cutBlind(-outer_height)
)
