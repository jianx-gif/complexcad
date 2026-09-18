import cadquery as cq
plate_width = 60.0
plate_height = 80.0
plate_thickness = 12.0
rib_height = 5.0
rib_width = 12.0
rib_thickness = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 6
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(rib_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (-hole_spacing / 2, -hole_spacing / 2),
    (hole_spacing / 2, -hole_spacing / 2),
    (-hole_spacing / 2, hole_spacing / 2),
    (hole_spacing / 2, hole_spacing / 2),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
