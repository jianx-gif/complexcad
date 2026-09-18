import cadquery as cq
import math
base_length = 80.0
base_width = 15.0
base_thickness = 5.0
rib_height = 2.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset_from_edge = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(base_length - 2 * rib_spacing, base_width - 2 * rib_spacing)
    .extrude(rib_height)
)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
combined = base.union(rib)
hole_positions = [
    (hole_offset_from_edge,  hole_offset_from_edge),
    (-hole_offset_from_edge,  hole_offset_from_edge),
    (hole_offset_from_edge, -hole_offset_from_edge),
    (-hole_offset_from_edge, -hole_offset_from_edge),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
