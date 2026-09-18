import cadquery as cq
plate_length = 80.0
plate_width = 40.0
plate_thickness = 3.0
rib_height = 20.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_from_edge = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness, centered=(True, True, False))
    .shell(-plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .box(rib_width, plate_width, rib_height, centered=(True, True, False))
    .translate((0, 0, plate_thickness))
)
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
hole_positions = [
    (-hole_spacing/2, -hole_spacing/2),
    ( hole_spacing/2, -hole_spacing/2),
    ( hole_spacing/2, hole_spacing/2),
    (-hole_spacing/2, hole_spacing/2),
    ( hole_spacing/2, hole_spacing/2)
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
    .edges()
    .chamfer(chamfer_size)
)
