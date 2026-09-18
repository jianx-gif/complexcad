import cadquery as cq
outer_diameter = 80.0
inner_diameter = 40.0
thickness = 20.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 4.0
rib_count = 6
chamfer_size = 1.0
mount_hole_dia = 4.0
mount_hole_spacing = 30.0
rib_count = 4
rib_radius = outer_diameter / 2.0
rib_count = 3
rib_radius = rib_radius + rib_thickness
rib_height = thickness * 0.6
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(thickness)
)
rib = rib.translate((rib_radius, 0, 0))
)
rib = rib.translate((rib_radius, 0, 0))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(mount_hole_dia)
result = combined
