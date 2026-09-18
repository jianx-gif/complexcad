import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 2.0
rib_height = 12.0
rib_width = 4.0
rib_thickness = 2.0
rib_spacing = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, 0)
    .close()
    .revolve()
)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_thickness / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces("<Z").workplane().center(0, 0).hole(rib_thickness)
result = combined
