import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_height = 5.0
rib_width = 6.0
rib_thickness = 2.0
rib_spacing = 12.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset = 15.0
chamfer_size = 0.5
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
rib = rib.edges("|Z").chamfer(chamfer_size)
rib1 = rib.translate((inner_diameter / 2 + rib_thickness / 2, 0, 0))
rib2 = rib.translate((inner_diameter / 2 + rib_thickness / 2, 0, 0))
rib3 = rib.translate((inner_diameter / 2 + rib_thickness / 2, 0, 0))
rib4 = rib.translate((inner_diameter / 2 + rib_thickness / 2, 0, 0))
rib1 = rib.translate((inner_diameter / 2 + rib_thickness / 2, 0, 0))
rib2 = rib1.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib3 = rib2.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib1 = rib2.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib2 = rib1.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib3 = rib1.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib1 = rib2.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib2 = rib1.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib3 = rib1.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib1 = rib1.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib2 = rib1.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib2 = rib1.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib3 = rib2.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib1 = rib1.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib2 = rib1.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib2 = rib1.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib3 = rib2.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib1 = rib3.union(rib2)
result = (
    cq.Workplane("XY")
    .rect(rib_width, rib_thickness)
    .extrude(thickness)
    .translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
)
