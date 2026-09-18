import cadquery as cq
outer_radius = 45.0
inner_radius = 20.0
wall_thickness = 2.0
rib_height = 5.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 0.5
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius + wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(base_height)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(rib_height)
    .translate((0, 0, base_height))
)
base = base.union(rib)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(rib_height)
    .translate((0, 0, base_height))
)
base = base.union(rib)
base = base.edges("|Z").chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_width)
    .translate((0, 0, base_height))
)
base = base.union(rib)
base = base.edges(">Z").chamfer(chamfer_size)
result = base
