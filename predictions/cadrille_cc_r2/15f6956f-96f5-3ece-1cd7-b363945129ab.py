import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
rib_width = 12.0
rib_height = 4.0
hole_diameter = 6.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 1.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 15.0
rib_length = plate_length - 2 * rib_width
rib_width = plate_width - 2 * rib_width
rib_height = plate_thickness - 2 * rib_width
rib_count = int((plate_width - rib_width) // rib_length)
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
base = base.edges("|Z").chamfer(chamfer_size)
rib = (
    base.faces(">Z")
    .workplane()
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)
base = base.union(rib)
hole_positions = [
    (-hole_spacing_x/2, hole_spacing_y/2),
    (hole_spacing_x/2, hole_spacing_y/2),
    (-hole_spacing_x/2, hole_spacing_y/2),
    (hole_spacing_x/2, hole_spacing_y/2),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)
base = base.edges("|Z").chamfer(chamfer_size)
result = base
