import cadquery as cq
plate_length = 80.0
plate_width = 100.0
plate_thickness = 8.0
rib_height = 6.0
rib_width = 10.0
rib_fillet_radius = 1.0
hole_diameter = 6.0
hole_spacing_x = 20.0
hole_spacing_y = 30.0
hole_rows = 2
hole_cols = 3
chamfer_size = 1.0
pocket_depth = 4.0
pocket_margin = 5.0
pocket_width = 20.0
pocket_depth = plate_thickness - 2.0
rib_width = 10.0
rib_height = 6.0
rib_fillet_radius = 1.0
base_plate = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .fillet(rib_fillet_radius)
)
base_plate = base_plate.edges("|Z").chamfer(chamfer_size)
rib = (
    base_plate.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
hole_positions = [
    (-hole_spacing_x/2, -hole_spacing_y/2),
    (hole_spacing_x/2, -hole_spacing_y/2),
    (-hole_spacing_x/2, hole_spacing_y/2),
    (hole_spacing_x/2, hole_spacing_y/2),
]
base_plate = (
    base_plate.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
rib = (
    base_plate.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = base_plate.union(rib)
