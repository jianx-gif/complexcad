import cadquery as cq
import math
base_radius = 12.0
base_height = 8.0
base_thickness = 5.0
rib_height = 4.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 3
chamfer_distance = 0.5
hole_diameter = 5.0
hole_spacing = 30.0
hole_count = 4
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_distance)
hole_positions = [
    (hole_offset,  hole_offset),
    (-hole_offset,  hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, -hole_offset),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
