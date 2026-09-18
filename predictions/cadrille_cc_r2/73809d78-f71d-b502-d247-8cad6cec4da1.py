import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 6
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
rib = rib.edges("|Z").chamfer(chamfer_distance)
rib1 = rib.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib2 = rib.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib3 = rib.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib4 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib5 = rib4.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib6 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib3 = rib6.rotate((0, 0, 0), (0, 0, 1), 90)
rib5 = rib3.union(rib6)
rib1 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib2 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib3 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib5 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib6 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib1 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib2 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib3 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib1 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib2 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib3 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib1 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib2 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib3 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib1 = rib3.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib2 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib3 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib1 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib2 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib3 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib1 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib2 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib3 = rib1.translate((inner_radius + wall_thickness/2.0, 0, 0))
rib1 = rib1.translate((inner_radius