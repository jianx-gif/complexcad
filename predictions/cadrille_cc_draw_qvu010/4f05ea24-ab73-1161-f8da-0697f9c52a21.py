import cadquery as cq
plate_width = 80.0
plate_height = 60.0
plate_thickness = 5.0
rib_height = 12.0
rib_width = 10.0
rib_thickness = 2.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 15.0
chamfer_size = 0.5
base = cq.Workplane('XY').rect(plate_width, plate_height).extrude(plate_thickness)
rib = (
    cq.Workplane('XY')
    .rect(rib_width, plate_height)
    .extrude(rib_thickness)
    .translate((0, 0, plate_thickness))
)
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
hole_positions = [
    (-hole_spacing/2, -hole_offset),
    (hole_spacing/2, -hole_offset),
    (-hole_spacing/2, hole_offset),
    (hole_spacing/2, hole_offset),
]
result = (
    combined
    .faces('>Z')
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
