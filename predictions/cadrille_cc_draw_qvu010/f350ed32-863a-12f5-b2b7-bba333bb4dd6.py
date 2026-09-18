import cadquery as cq
plate_length = 60.0
plate_width = 30.0
plate_thickness = 6.0
rib_height = 4.0
rib_width = 12.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 6
chamfer_size = 0.5
base = cq.Workplane('XY').box(plate_length, plate_width, plate_thickness)
rib = (
    base.faces('>Z')
    .workplane()
    .rect(rib_width, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
)
rib = rib.faces('>Z').edges().chamfer(chamfer_size)
rib = (
    rib.faces('>Z')
    .workplane()
    .rect(rib_width, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
)
result = base.union(rib)
hole_positions = [
    (-hole_spacing / 2, -hole_spacing / 2),
    (hole_spacing / 2, -hole_spacing / 2),
    (-hole_spacing / 2, hole_spacing / 2),
    (hole_spacing / 2, hole_spacing / 2),
]
result = (
    result.faces('>Z')
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = result.edges('|Z').chamfer(chamfer_size)
