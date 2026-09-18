import cadquery as cq
import math
base_length = 80.0
base_width = 30.0
base_thickness = 8.0
wall_thickness = 2.0
rib_width = 10.0
rib_height = 4.0
rib_spacing = 12.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 4
hole_offset = 15.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(base_length - 2 * wall_thickness, base_width - 2 * wall_thickness)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(base_length - 2 * wall_thickness, base_width - 2 * wall_thickness)
    .extrude(base_thickness)
)
combined = base.union(rib)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (hole_offset, 0)
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = (
    combined
    .edges("|Z")
    .chamfer(chamfer_size)
)
