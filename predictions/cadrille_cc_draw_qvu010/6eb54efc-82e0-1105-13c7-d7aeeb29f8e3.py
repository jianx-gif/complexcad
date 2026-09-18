import cadquery as cq
plate_width = 80.0
plate_depth = 40.0
plate_thickness = 8.0
rib_height = 6.0
rib_width = 12.0
rib_thickness = 4.0
hole_diameter = 6.0
hole_spacing = 30.0
hole_count = 6
hole_offset = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(rib_height)
)
rib = (
    base.faces(">Z").workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
combined = base.union(rib)
hole_positions = [
    (-hole_spacing / 2, -hole_offset),
    (hole_spacing / 2, -hole_offset),
    (-hole_spacing / 2, hole_offset),
    (hole_spacing / 2, hole_offset),
]
combined = (
    combined.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
combined = (
    combined.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
combined = (
    combined.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
