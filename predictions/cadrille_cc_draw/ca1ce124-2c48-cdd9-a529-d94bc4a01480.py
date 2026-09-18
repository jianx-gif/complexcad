import cadquery as cq
import math
base_width = 40.0
base_height = 30.0
base_thickness = 8.0
rib_height = 12.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
rib_count = 6
rib_count = 8
rib_margin = 5.0
chamfer_size = 1.0
rib_count = 4
rib_count = 6
rib_count = 4
base = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(base_width - 2 * rib_margin, base_height - 2 * rib_margin)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).rect(rib_width, rib_height).cutBlind(-rib_height)
result = combined
