import cadquery as cq
import math
outer_diameter = 60.0
wall_thickness = 4.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
fillet_radius = 2.0
chamfer_distance = 1.0
rib_thickness = 2.0
rib_height = 10.0
rib_width = 6.0
rib_count = 6
outer_radius = outer_diameter / 2.0
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_radius)
    .faces(">Z")
    .workplane()
    .hole(inner_radius)
)
rib = (
    cq.Workplane("XY")
    .center(inner_radius + rib_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = rib.translate((inner_radius + rib_thickness / 2.0, 0, 0)))
rib = rib.translate((inner_radius + rib_thickness / 2.0, 0, 0))
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([
        (inner_radius + rib_thickness / 2.0, inner_radius + rib_thickness / 2.0),
        (inner_radius + rib_thickness / 2.0, inner_radius + rib_thickness / 2.0),
        (inner_radius, inner_radius + rib_thickness / 2.0),
        (inner_radius, inner_radius + rib_thickness / 2.0),
    ])
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
combined = combined.union(rib)
result = combined
