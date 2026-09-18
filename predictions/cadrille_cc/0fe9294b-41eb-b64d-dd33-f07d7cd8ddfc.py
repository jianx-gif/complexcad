import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 15.0
fillet_radius = 2.0
chamfer_distance = 1.0
hole_diameter = 5.0
hole_depth = 10.0
hole_offset = 15.0
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
    .center(inner_radius + rib_spacing / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(inner_radius + rib_spacing / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
base = base.union(base)
result = base
