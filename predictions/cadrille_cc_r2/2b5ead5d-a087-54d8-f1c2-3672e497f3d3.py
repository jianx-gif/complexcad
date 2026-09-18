import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset = 15.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = rib.edges("|Z").chamfer(chamfer_distance)
rib1 = rib.translate((inner_diameter / 2 + rib_width / 2, 0, 0))
rib2 = rib.translate((inner_diameter / 2 + rib_width / 2, 0, 0))
rib3 = rib.translate((inner_diameter / 2 + rib_width / 2, 0, 0))
rib4 = rib1.translate((inner_diameter / 2 + rib_width / 2, 0, 0))
rib5 = rib4.translate((inner_diameter / 2 + rib_width / 2, 0, 0))
rib6 = rib4.translate((inner_diameter / 2 + rib_width / 2, 0, 0))
rib1 = rib1.translate((inner_diameter / 2 + rib_width / 2, 0, 0))
rib2 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib3 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib1 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib2 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib3 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib1 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib2 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib3 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib1 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib2 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib1 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib2 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib3 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib1 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib2 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib2 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib1 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib2 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib2 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib3 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
rib1 = rib1.translate((inner_diameter / 2 - rib_width / 2, 0, 0))
