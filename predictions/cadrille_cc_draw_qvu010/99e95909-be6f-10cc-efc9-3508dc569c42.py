import cadquery as cq
plate_width = 80.0
plate_depth = 40.0
plate_thickness = 5.0
rib_height = 8.0
rib_width = 12.0
rib_thickness = 2.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (-hole_spacing / 2, -hole_offset),
    (hole_spacing / 2, -hole_offset),
    (-hole_spacing / 2, hole_offset),
    (hole_spacing / 2, hole_offset),
    (-hole_spacing / 2, hole_offset),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
result = combined
