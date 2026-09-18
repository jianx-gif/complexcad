import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 10.0
wall_thickness = 2.0
rib_width = 4.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_distance = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius + wall_thickness
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
rib1 = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib2 = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib3 = rib1.union(rib1).union(rib2)
rib1 = rib3.translate((0, 0, thickness - wall_thickness))
rib2 = rib1.translate((0, 0, thickness - wall_thickness))
rib3 = rib1.translate((0, 0, thickness - wall_thickness))
rib1 = rib2.translate((0, 0, thickness - wall_thickness))
rib2 = rib1.translate((0, 0, thickness - wall_thickness))
rib3 = rib2.translate((0, 0, thickness - wall_thickness))
combined = base.union(rib1).union(rib2)
combined = combined.edges("|Z").chamfer(chamfer_distance)
result = combined
