import cadquery as cq
outer_diameter = 60.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
rib_width = 4.0
rib_height = 1.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
rib_count = 6
rib_radius = inner_radius + rib_height / 2.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(outer_diameter / 2.0)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(rib_thickness)
)
rib = rib.translate((rib_radius, 0, 0))
rib = rib.translate((rib_radius, 0, 0))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
result = combined
