import cadquery as cq
outer_diameter = 50.0
inner_diameter = 30.0
thickness = 40.0
rib_height = 8.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
rib_spacing = 12.0
chamfer_size = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(inner_radius - rib_width / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.edges().chamfer(chamfer_size)
rib = (
    rib.faces(">Z")
    .workplane()
    .center(inner_radius - rib_width / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_width)
)
rib = rib.translate((outer_radius - rib_width / 2.0, 0, 0))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
result = combined
