import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 30.0
rib_height = 5.0
rib_width = 10.0
rib_thickness = 4.0
rib_count = 6
chamfer_size = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius - inner_radius
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.edges(">Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
rib = (
    cq.Workplane("XY")
    .center(inner_radius + rib_thickness / 2.0, 0)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
combined = combined.union(rib)
combined = combined.edges(">Z").chamfer(chamfer_size)
result = combined
