import cadquery as cq
base_length = 80.0
base_width = 40.0
base_thickness = 20.0
wall_thickness = 2.0
rib_width = 12.0
rib_height = 8.0
rib_spacing = 15.0
rib_count = 6
rib_count = 8
rib_count = 4
rib_spacing = 12.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(base_length - 2 * wall_thickness, base_width - 2 * wall_thickness)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.edges(">Z").chamfer(chamfer_size)
result = combined
