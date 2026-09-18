import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
wall_thickness = 3.0
inner_radius = outer_diameter / 2.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_radius - wall_thickness
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(wall_thickness)
)
inner = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(wall_thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius - rib_thickness)
    .extrude(wall_thickness)
)
rib = rib.union(rib)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(wall_thickness + rib_height)
    .translate((inner_radius + rib_thickness / 2.0, 0, wall_thickness))
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
