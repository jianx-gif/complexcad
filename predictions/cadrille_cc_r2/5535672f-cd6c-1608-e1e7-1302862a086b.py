import cadquery as cq
outer_diameter = 80.0
inner_diameter = 60.0
thickness = 10.0
rib_height = 5.0
rib_width = 12.0
rib_thickness = 4.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 15.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = rib.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib = rib.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib = rib.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib = rib.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib = rib.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib = rib.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
rib = rib.translate((inner_diameter / 2 - rib_thickness / 2, 0, 0))
result = base.union(rib)
result = result.edges("|Z").chamfer(chamfer_size)
