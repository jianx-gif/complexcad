import cadquery as cq
import math
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_depth = thickness - 2.0
chamfer_size = 0.5
hole_spacing = 20.0
hole_count = 4
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2 - rib_width / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, thickness / 2))
rib = rib.translate((0, 0, thickness / 2))
rib = rib.translate((0, 0, thickness / 2))
rib = rib.translate((0, 0, thickness / 2))
rib = rib.translate((0, 0, thickness / 2))
rib = rib.translate((0, 0, thickness / 2 - rib_height / 2))
rib = rib.translate((0, 0, thickness / 2 - rib_height / 2))
result = base.union(rib)
result = result.edges("|Z").chamfer(chamfer_size)
result = result.faces(">Z").workplane().hole(hole_diameter, depth=hole_depth)
result = result.faces(">Z").workplane().center(hole_spacing, 0).hole(hole_diameter, depth=hole_depth)
