import cadquery as cq

outer_radius = 45.0
inner_radius = 30.0
thickness = 10.0
groove_width = 4.0
groove_depth = 2.0
fillet_radius = 1.5
hole_diameter = 4.5
hole_count = 6
hole_circle_radius = (inner_radius + outer_radius) / 2.0

base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(thickness)
)

groove = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(outer_radius - groove_width)
    .extrude(groove_depth)
)

result = (
    base
    .cut(groove)
    .edges()
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .polarArray(radius=hole_circle_radius, count=hole_count, startAngle=0, angle=360)
    .hole(hole_diameter)
)
