import cadquery as cq
plate_length = 80.0
plate_width = 80.0
plate_thickness = 6.0
rib_height = 4.0
rib_width = 10.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 20.0
chamfer_size = 1.0
base_plate = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)
rib = (
    cq.Workplane("XY")
    .box(rib_width, plate_width, plate_thickness)
    .translate((0, 0, plate_thickness/2))
)
combined = base_plate.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (-hole_spacing_x/2, -hole_spacing_y/2),
    (hole_spacing_x/2, -hole_spacing_y/2),
    (-hole_spacing_x/2, hole_spacing_y/2),
]
combined = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined.edges("|Z").chamfer(chamfer_size)
