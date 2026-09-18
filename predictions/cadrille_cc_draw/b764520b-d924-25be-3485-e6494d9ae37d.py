import cadquery as cq
outer_radius = 15.0
inner_radius = 15.0
height = 80.0
wall_thickness = 2.0
rib_width = 4.0
rib_height = 10.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 0.5
outer = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
    .translate((outer_radius - rib_thickness/2, 0, 0))
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
    .translate((outer_radius - rib_thickness/2, 0, 0))
)
combined = outer.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
result = combined
