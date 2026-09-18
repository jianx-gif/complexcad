import cadquery as cq
outer_diameter = 30.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
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
    .circle(outer_radius)
    .extrude(rib_height)
    .translate((0, 0, wall_thickness))
)
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, -rib_height))
combined = base.union(rib)
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
result = combined
