import cadquery as cq
import math
base_length = 100.0
base_width = 20.0
base_thickness = 10.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset_from_end = 15.0
chamfer_distance = 1.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .rect(base_length - 2 * wall_thickness, base_width - 2 * wall_thickness)
    .cutBlind(-base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(base_length - 2 * wall_thickness, rib_width)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
base = base.union(rib)
hole_positions = [
    (hole_offset_from_end - hole_offset_from_end) / 2,
    (hole_offset_from_end - hole_offset_from_end) / 2,
    (-hole_offset_from_end + hole_offset_from_end) / 2,
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
result = base.union(rib)
