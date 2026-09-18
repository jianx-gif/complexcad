import cadquery as cq
import math
outer_diameter = 12.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
chamfer_size = 0.5
rib_width = 4.0
rib_height = 1.5
rib_thickness = 1.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
rib_radius = inner_radius + rib_thickness / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(outer_diameter)
)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = rib.translate((outer_diameter / 2.0, 0, 0))
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
