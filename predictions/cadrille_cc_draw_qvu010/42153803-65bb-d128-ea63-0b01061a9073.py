import cadquery as cq
import math
base_length = 80.0
base_width = 40.0
base_thickness = 10.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 12.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_spacing = 12.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
base = base.edges("|Z").chamfer(chamfer_size)
rib_count = int(base_length / rib_spacing)
rib = (
    base.faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_width)
)
rib = rib.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_width)
rib = rib.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_width)
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
