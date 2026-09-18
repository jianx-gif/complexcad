import cadquery as cq
plate_length = 100.0
plate_width = 40.0
plate_thickness = 8.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 20.0
hole_rows = 2
hole_cols = 3
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)
rib = (
    cq.Workplane("XY")
    .box(rib_width, plate_width, plate_thickness)
    .translate((0, plate_width / 2 + rib_spacing / 2, 0))
)
rib_pattern = rib.translate((0, plate_width / 2 + rib_spacing / 2, 0))
rib_pattern = rib_pattern.union(rib_pattern)
result = (
    base.union(rib_pattern)
    .faces(">Z")
    .workplane()
    .center(0, hole_spacing / 2)
    .rect(rib_width, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
)
result = result.union(rib_pattern)
result = (
    result.faces(">Z")
    .workplane()
    .center(hole_cols - hole_spacing / 2, hole_cols - hole_spacing / 2)
    .hole(hole_diameter)
)
