import cadquery as cq
import math
base_width = 60.0
base_height = 30.0
base_thickness = 8.0
rib_height = 12.0
rib_width = 10.0
rib_thickness = 4.0
rib_spacing = 15.0
hole_diameter = 6.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 1.0
profile = (
    cq.Workplane("XY")
    .moveTo(base_width/2, 0)
    .lineTo(base_width/2, base_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_height)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2, base_height + rib_width)
    .lineTo(base_width/2,