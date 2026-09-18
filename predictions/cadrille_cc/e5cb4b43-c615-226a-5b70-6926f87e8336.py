import cadquery as cq
plate_width = 80.0
plate_height = 80.0
plate_thickness = 6.0
rib_width = 4.0
rib_height = 3.0
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
    .box(plate_width, plate_height, plate_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, plate_thickness)
    .translate((0, 0, plate_thickness/2))
)
combined = base.union(rib)
hole_positions = [
    (-hole_spacing_x/2, -hole_spacing_y/2),
    (hole_spacing_x/2, -hole_spacing_y/2),
    (-hole_spacing_x/2, hole_spacing_y/2),
    (hole_spacing_x/2, hole_spacing_y/2),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = (
    combined
    .faces(">Z")
    .workplane()
    .center(hole_spacing_x/2, hole_spacing_y/2)
    .hole(hole_diameter)
)
