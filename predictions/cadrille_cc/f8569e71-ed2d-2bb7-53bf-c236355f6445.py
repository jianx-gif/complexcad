import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 12.0
fillet_radius = 2.0
chamfer_distance = 0.5
hole_diameter = 5.0
hole_spacing = 12.0
hole_count = 6
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 4
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_width)
    .translate((0, 0, thickness))
)
base = base.union(rib)
base = base.edges("|Z").fillet(fillet_radius)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (-hole_offset, -hole_offset),
    (hole_offset, -hole_offset),
]
base = base.faces(">Z").workplane().pushPoints(hole_positions).hole(hole_diameter)
result = base
