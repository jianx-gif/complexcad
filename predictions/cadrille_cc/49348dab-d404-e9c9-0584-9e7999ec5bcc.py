import cadquery as cq
import math
plate_length = 60.0
plate_width = 40.0
plate_thickness = 8.0
rib_width = 4.0
rib_height = 3.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 6
hole_offset = 10.0
chamfer_size = 0.5
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
rib_pattern = rib.translate((0, plate_width/2 - rib_width/2, plate_thickness))
rib_pattern = rib.translate((0, plate_width/2 - rib_width/2, plate_thickness))
rib_pattern = rib_pattern.union(rib_pattern)
rib_pattern = rib_pattern.faces(">Z").workplane().hole(hole_diameter)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, plate_width).extrude(rib_height)
rib_pattern = rib_pattern.union(rib_pattern)
result = rib_pattern
