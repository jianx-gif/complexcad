import cadquery as cq
import math
plate_length = 80.0
plate_width = 30.0
plate_thickness = 5.0
rib_width = 12.0
rib_height = 8.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_length - 2 * rib_spacing, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
)
rib = rib.translate((0, plate_width/2 - rib_width/2, plate_thickness/2))
combined = base.union(rib)
hole_positions = [
    (-hole_offset, -hole_offset),
    (hole_offset, -hole_offset),
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
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
    .center(hole_offset, hole_offset)
    .hole(hole_diameter)
)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
