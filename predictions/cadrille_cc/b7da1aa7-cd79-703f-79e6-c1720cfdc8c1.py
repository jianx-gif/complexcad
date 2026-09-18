import cadquery as cq
import math
plate_length = 80.0
plate_width = 50.0
plate_thickness = 8.0
rib_width = 12.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 6
hole_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .circle(plate_length)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_length, rib_width)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
rib_pattern = rib.translate((0, plate_width/2 - rib_width/2, plate_thickness))
rib_pattern = rib_pattern.union(rib_pattern)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_width)
    .extrude(rib_height)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (-hole_offset, -hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, hole_offset),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
