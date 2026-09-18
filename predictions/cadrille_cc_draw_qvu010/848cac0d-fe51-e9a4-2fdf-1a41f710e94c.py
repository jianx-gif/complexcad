import cadquery as cq
import math
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 25.0
rib_height = 5.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_radius = outer_diameter / 2.0
rib_count = 6
chamfer_distance = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_distance)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().polarArray(radius=outer_radius - rib_radius, count=rib_count, startAngle=0, angle=360).hole(inner_diameter)
combined = combined.faces(">Z").workplane().polarArray(radius=outer_radius - rib_radius, count=rib_count, startAngle=0, angle=360).hole(inner_diameter)
result = combined
