import cadquery as cq
outer_diameter = 60.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = inner_diameter / 2.0
rib_width = 10.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 15.0
chamfer_size = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_diameter)
)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(rib_height)
    .translate((0, 0, wall_thickness))
)
rib = rib.translate((outer_radius, 0, wall_thickness))
rib = rib.translate((outer_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
rib = rib.translate((inner_radius, 0, wall_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
result = combined
