import cadquery as cq
import math

outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
groove_width = 5.0
groove_depth = 2.0
hole_diameter = 6.0
hole_count = 6
hole_radius = (outer_diameter/2) - 8.0
chamfer_size = 1.0
fillet_radius = 0.8
rib_width = 4.0
rib_height = 2.0
rib_count = 4
rib_offset = 5.0

base = (
    cq.Workplane("XY")
    .sketch()
    .circle(outer_diameter/2)
    .circle(inner_diameter/2)
    .finalize()
    .extrude(thickness)
)

groove = (
    cq.Workplane("XY")
    .circle(outer_diameter/2)
    .circle((outer_diameter/2) - groove_width)
    .extrude(groove_depth)
    .translate((0, 0, thickness - groove_depth))
)

result = base.cut(groove)

hole_positions = [
    (
        hole_radius * math.cos(math.radians(i * 360.0 / hole_count)),
        hole_radius * math.sin(math.radians(i * 360.0 / hole_count))
    )
    for i in range(hole_count)
]

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .circle(hole_diameter/2)
    .cutBlind(-thickness)
)

result = result.faces(">Z").edges().chamfer(chamfer_size)

result = result.faces("<Z").edges().fillet(fillet_radius)

rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness/2)
)

for i in range(rib_count):
    angle = i * 360.0 / rib_count
    x = (inner_diameter/2 + rib_offset) * math.cos(math.radians(angle))
    y = (inner_diameter/2 + rib_offset) * math.sin(math.radians(angle))
    result = result.union(rib.translate((x, y, 0)))
