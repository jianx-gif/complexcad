import cadquery as cq
outer_radius = 30.0
wall_thickness = 10.0
inner_radius = outer_radius - wall_thickness
rib_height = 12.0
rib_thickness = 5.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
chamfer_size = 0.5
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, rib_height)
    .lineTo(inner_radius + rib_thickness, rib_height)
    .lineTo(inner_radius + rib_thickness, rib_height + rib_height)
    .lineTo(inner_radius, rib_height + rib_height)
    .lineTo(inner_radius, 0)
    .close()
    .revolve()
)
base = base.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(inner_radius + rib_thickness/2, rib_height/2)
    .rect(rib_thickness, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((inner_radius + rib_thickness/2, 0, 0))
rib = rib.translate((inner_radius + rib_thickness/2, 0, 0))
combined = base.union(rib)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
result = combined
