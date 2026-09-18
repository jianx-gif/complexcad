import cadquery as cq
outer_radius = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
wall_thickness = 2.0
rib_thickness = 2.0
rib_height = 10.0
rib_width = 4.0
rib_spacing = 12.0
chamfer_distance = 0.5
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(wall_thickness)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_thickness, rib_height)
    .extrude(wall_thickness)
)
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_distance)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
result = combined
