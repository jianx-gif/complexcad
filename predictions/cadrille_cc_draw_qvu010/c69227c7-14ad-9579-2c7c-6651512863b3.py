import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 12.0
rib_width = 6.0
rib_height = 8.0
rib_thickness = 4.0
rib_count = 6
chamfer_size = 1.0
hole_diameter = 4.0
hole_depth = 6.0
hole_count = 8
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2, 0)
    .lineTo(inner_diameter / 2, thickness - rib_height)
    .lineTo(inner_diameter / 2, thickness - rib_height)
    .lineTo(inner_diameter / 2, thickness - rib_height)
    .lineTo(inner_diameter / 2, thickness - rib_height)
    .lineTo(inner_diameter / 2, thickness)
    .lineTo(inner_diameter / 2, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(rib_thickness)
    .translate((0, 0, thickness / 2))
)
solid = solid.union(rib)
hole_positions = [
    (hole_count - 1) * hole_count * hole_count,
    (hole_count - 1) * hole_count * hole_count * hole_count * hole_count),
    (hole_count - 1) * hole_count * hole_count * hole_count * hole_count * hole_count))
]
solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = solid
