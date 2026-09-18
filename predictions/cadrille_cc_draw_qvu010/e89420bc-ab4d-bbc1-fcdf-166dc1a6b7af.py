import cadquery as cq
import math
base_width = 80.0
base_height = 40.0
base_thickness = 5.0
rib_width = 12.0
rib_height = 10.0
rib_thickness = 2.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 6
hole_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, base_height)
    .extrude(rib_thickness)
    .translate((0, 0, base_thickness))
)
rib = rib.translate((0, 0, base_thickness))
combined = base.union(rib)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (0, -hole_offset),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
