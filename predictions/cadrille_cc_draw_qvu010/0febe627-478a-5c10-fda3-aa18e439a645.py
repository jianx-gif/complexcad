import cadquery as cq
plate_width = 80.0
plate_depth = 60.0
plate_thickness = 6.0
rib_height = 4.0
rib_width = 12.0
rib_thickness = 4.0
hole_diameter = 6.0
hole_spacing = 30.0
hole_count = 6
hole_offset = 10.0
chamfer_size = 1.0
base = cq.Workplane('XY').box(plate_width, plate_depth, plate_thickness)
rib = (
    base.faces('>Z')
    .workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
rib = rib.faces('>Z').edges().chamfer(chamfer_size)
rib = (
    rib.faces('>Z')
    .workplane()
    .rect(plate_width - 2 * rib_width, plate_depth - 2 * rib_width)
    .extrude(rib_height)
)
result = base.union(rib)
hole_positions = [
    (-hole_spacing/2, -hole_offset),
    (hole_spacing/2, -hole_offset),
    (-hole_spacing/2, hole_offset),
    (hole_spacing/2, hole_offset),
]
result = (
    result.faces('>Z')
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = result.edges('|Z').chamfer(chamfer_size)
