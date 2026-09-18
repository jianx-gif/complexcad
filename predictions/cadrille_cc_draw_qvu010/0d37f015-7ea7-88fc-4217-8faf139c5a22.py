import cadquery as cq
import math
outer_diameter = 60.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
rib_width = 10.0
rib_height = 3.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_distance = 0.5
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(outer_diameter)
)
rib = (
    cq.Workplane("XY")
    .center(inner_radius, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = rib.translate((inner_radius + rib_thickness / 2.0, 0, 0))
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(inner_radius + rib_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
combined = combined.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_distance)
result = combined
