import cadquery as cq
outer_diameter = 40.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
rib_width = 8.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
rib_spacing = 12.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(wall_thickness)
)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2.0 - rib_spacing, 0)
    .rect(rib_width, rib_height)
    .extrude(wall_thickness)
)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2.0 - rib_spacing, 0)
    .rect(rib_width, rib_height)
    .extrude(wall_thickness)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
result = combined
