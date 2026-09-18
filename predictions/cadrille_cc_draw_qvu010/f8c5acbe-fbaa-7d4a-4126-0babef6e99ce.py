import cadquery as cq
import math
base_length = 80.0
base_width = 30.0
base_thickness = 10.0
wall_thickness = 2.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 15.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 6
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(base_length - 2 * wall_thickness, base_width - 2 * wall_thickness)
    .cutBlind(-base_thickness)
)
rib = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (hole_offset, hole_offset),
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
