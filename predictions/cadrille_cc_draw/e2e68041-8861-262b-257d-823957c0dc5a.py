import cadquery as cq
import math
base_width = 80.0
base_height = 30.0
base_thickness = 12.0
rib_width = 10.0
rib_height = 5.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_spacing = 20.0
rib_offset = 5.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_width)
    .translate((0, 0, base_thickness))
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_width)
    .translate((0, 0, base_thickness))
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).rect(rib_width, rib_height).cutBlind(-rib_width)
result = combined
