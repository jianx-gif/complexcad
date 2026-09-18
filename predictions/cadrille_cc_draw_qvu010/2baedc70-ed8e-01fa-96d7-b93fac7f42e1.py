import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 20.0
thickness = 5.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 0.5
hole_diameter = 4.0
hole_depth = thickness / 2.0
hole_spacing = 12.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2.0, 0)
    .lineTo(inner_diameter / 2.0, thickness)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, thickness + rib_height)
    .lineTo(inner_diameter / 2.0, 0)
    .close()
)
result = (
    profile
    .revolve(360)
    .edges()
    .chamfer(chamfer_size)
)
