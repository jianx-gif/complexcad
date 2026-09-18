import cadquery as cq
import math
plate_length = 80.0
plate_width = 40.0
plate_thickness = 8.0
rib_height = 12.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
rib_count = 6
rib_spacing = 15.0
rib_offset = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_length - 2 * rib_spacing, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, plate_thickness))
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(rib_count)
combined = combined.faces(">Z").workplane().center(0, 0).rect(rib_width, rib_height).extrude(rib_height)
combined = combined.union(rib)
result = combined
