import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 20.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_depth = thickness / 2.0
chamfer_size = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(inner_radius + rib_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((outer_radius - rib_thickness / 2.0, 0, 0))
combined = base.union(rib)
hole_positions = [
    (inner_radius + i * hole_spacing, 0),
    (inner_radius + j * hole_spacing, 0),
    (inner_radius + j * hole_spacing, 0),
    (inner_radius, 0),
]
for pos in hole_positions:
    combined = (
        combined
        .faces(">Z")
        .workplane()
        .pushPoints(hole_positions)
        .hole(hole_diameter)
    )
rib = (
    cq.Workplane("XY")
    .center(pos + j * rib_spacing / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
combined = combined.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
