import cadquery as cq
import math
base_radius = 15.0
base_height = 80.0
wall_thickness = 3.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
rib_count = 6
chamfer_distance = 1.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 4
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(base_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, base_height))
)
rib = rib.translate((0, 0, base_height + rib_height))
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
    .hole(hole_diameter)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
    .hole(hole_diameter)
)
result = combined
