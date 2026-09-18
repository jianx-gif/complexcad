import cadquery as cq
import math
base_length = 80.0
base_width = 20.0
base_thickness = 15.0
wall_thickness = 2.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_count = 6
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(base_length - 2 * wall_thickness, base_width - 2 * wall_thickness)
    .cutBlind(-base_thickness)
)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, hole_offset),
    (-hole_offset, hole_offset),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(base_length - 2 * wall_thickness, base_width - 2 * wall_thickness)
    .cutBlind(-base_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(base_length - 2 * wall_thickness, base_width - 2 * wall_thickness)
    .cutBlind(-base_thickness)
)
result = base
