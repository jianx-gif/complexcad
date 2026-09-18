import cadquery as cq
base_length = 80.0
base_width = 60.0
base_thickness = 12.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 20.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
result = base.union(rib)
result = result.edges("|Z").chamfer(chamfer_size)
