import cadquery as cq
import math
base_width = 60.0
base_height = 30.0
base_thickness = 5.0
wall_thickness = 2.0
rib_width = 12.0
rib_height = 8.0
rib_spacing = 12.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_depth = 4.0
hole_spacing = 15.0
hole_count = 6
hole_count = 4
base = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
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
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (hole_count - 1) * hole_spacing, 0) for i in range(hole_count)
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
