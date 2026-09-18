import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 20.0
thickness = 10.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 6
hole_radius = hole_diameter / 2.0
rib_width = 8.0
rib_height = 3.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 6
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib1 = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib2 = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib3 = rib2.union(rib1).union(rib2)
rib1 = rib3.translate((0, rib_spacing, 0))
rib2 = rib1.translate((0, rib_spacing, 0))
rib3 = rib2.translate((0, -rib_spacing, 0))
rib1 = rib2.translate((0, rib_spacing, 0))
rib2 = rib2.translate((0, -rib_spacing, 0))
rib3 = rib2.translate((0, -rib_spacing, 0))
rib1 = rib2.workplane(offset=thickness).center(0, 0).rect(rib_width, rib_height).extrude(rib_thickness)
rib2 = rib1.translate((0, rib_spacing, 0))
rib3 = rib2.translate((0, rib_spacing, 0))
rib1 = rib2.translate((0, rib_spacing, 0))
rib2 = rib2.translate((0, rib_spacing, 0))
rib3 = rib2.translate((0, rib_spacing, 0))
rib1 = rib2.workplane(offset=thickness).center(0, 0).rect(rib_width, rib_height).extrude(rib_thickness)
result = rib1.union(rib1).union(rib2)
