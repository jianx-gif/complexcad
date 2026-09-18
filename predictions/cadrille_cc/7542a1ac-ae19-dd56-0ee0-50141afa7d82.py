import cadquery as cq
outer_radius = 30.0
wall_thickness = 4.0
inner_radius = outer_radius - wall_thickness
base_thickness = 10.0
rib_height = 6.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .box(outer_radius, outer_radius, base_thickness, centered=(True, True, False))
    .faces(">Z")
    .workplane()
    .rect(outer_radius - wall_thickness, outer_radius - wall_thickness)
    .cutBlind(-wall_thickness)
)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, rib_width)
    .translate((outer_radius - rib_width/2, 0, rib_count))
)
rib_pattern = rib.translate((outer_radius - rib_width/2, 0, rib_count))
rib_pattern = rib_pattern.union(rib_pattern)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, rib_width)
    .translate((outer_radius - rib_width/2, 0, rib_count))
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
