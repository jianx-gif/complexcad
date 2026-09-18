import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 8.0
fillet_radius = 2.0
chamfer_distance = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
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
    .extrude(rib_thickness)
    .translate((inner_radius + rib_width / 2.0, 0, 0))
)
base = base.union(rib)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(outer_radius - rib_width / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
base = base.union(rib)
base = base.edges("|Z").fillet(fillet_radius)
result = base
