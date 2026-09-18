import cadquery as cq
plate_length = 80.0
plate_width = 50.0
plate_thickness = 8.0
rib_width = 4.0
rib_height = 3.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 12.0
hole_spacing_y = 15.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)
rib = (
    cq.Workplane("XY")
    .box(rib_width, plate_length, rib_height)
    .translate((0, plate_width / 2 + rib_spacing / 2, 0))
)
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, plate_width / 2 + rib_spacing / 2)
    .rect(rib_width, plate_width)
    .extrude(rib_height)
)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
