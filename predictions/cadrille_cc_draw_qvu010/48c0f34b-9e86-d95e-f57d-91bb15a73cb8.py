import cadquery as cq
import math
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 4.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
rib_count = 6
chamfer_distance = 0.5
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
    .translate((0, 0, thickness))
)
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_distance)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().polarArray(radius=inner_radius - rib_thickness/2, count=rib_count, startAngle=0, angle=360).hole(inner_diameter)
combined = combined.faces(">Z").workplane().polarArray(radius=inner_radius, startAngle=0, angle=360, count=rib_count).hole(inner_diameter)
result = combined
