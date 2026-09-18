import cadquery as cq
import math
base_length = 80.0
base_width = 50.0
base_thickness = 5.0
frame_height = 10.0
frame_thickness = 5.0
hole_diameter = 6.0
hole_spacing = 30.0
hole_count = 6
hole_offset = 15.0
chamfer_size = 0.5
rib_width = 12.0
rib_height = 4.0
rib_spacing = 12.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .rect(base_length - 2 * frame_thickness, base_width - 2 * frame_thickness)
    .cutBlind(-frame_height)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(base_length - 2 * frame_thickness, base_width - 2 * frame_thickness)
    .cutBlind(-frame_height)
)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (hole_offset, -hole_offset),
]
base = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, base_width)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
rib = rib.translate((0, 0, base_thickness))
result = base.union(rib)
