import cadquery as cq
plate_length = 80.0
plate_width = 40.0
plate_thickness = 4.0
rib_width = 6.0
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
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
)
rib = rib.translate((0, plate_width/2 - rib_spacing/2, plate_thickness/2))
combined = base.union(rib)
combined = (
    combined.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(plate_length - 2 * hole_spacing, plate_width - 2 * hole_spacing)
    .cutBlind(-plate_thickness)
)
combined = (
    combined.faces(">Z")
    .workplane()
    .center(hole_cols - hole_spacing, 0)
    .hole(hole_diameter)
)
result = combined.edges("|Z").chamfer(chamfer_size)
