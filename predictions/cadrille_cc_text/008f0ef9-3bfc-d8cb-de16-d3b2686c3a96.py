import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
rib_height = 3.0
rib_offset = 5.0
hole_diameter = 8.0
countersink_diameter = 12.0
countersink_angle = 82.0
hole_spacing_x = 20.0
hole_spacing_y = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing_y = 20.0
chamfer_size = 0.8
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_length - 2 * rib_offset, plate_width - 2 * rib_offset)
    .extrude(rib_height)
)
base = base.union(rib)
base = base.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (hole_spacing_x, hole_spacing_y),
    (-hole_spacing_x, hole_spacing_y),
    (hole_spacing_x, -hole_spacing_y),
    (-hole_spacing_x, -hole_spacing_y),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle)
)
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle)
)
rib = (
    base.faces(">Z")
    .workplane()
    .rect(rib_offset, plate_width - 2 * rib_offset)
    .extrude(rib_height)
)
result = base.union(rib)
