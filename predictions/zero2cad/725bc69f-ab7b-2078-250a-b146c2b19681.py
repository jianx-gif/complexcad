import cadquery as cq
from math import sin, cos, pi, floor

def hypocycloid(t, r1, r2):
    return (
        (r1 - r2) * cos(t) + r2 * cos(r1 / r2 * t - t),
        (r1 - r2) * sin(t) + r2 * sin(-(r1 / r2 * t - t))
    )

def epicycloid(t, r1, r2):
    return (
        (r1 + r2) * cos(t) - r2 * cos(r1 / r2 * t + t),
        (r1 + r2) * sin(t) - r2 * sin(r1 / r2 * t + t)
    )

def gear_curve(t, r1=12, r2=2):
    if (-1) ** (1 + floor(t / 2 / pi * (r1 / r2))) < 0:
        return epicycloid(t, r1, r2)
    else:
        return hypocycloid(t, r1, r2)

gear_height = 20.0
twist_angle = 180.0
central_hole_diameter = 4.0
tab_width = 6.0
tab_height = 10.0
tab_length = 20.0
chamfer_distance = 1.0

gear_body = (
    cq.Workplane("XY")
    .parametricCurve(lambda t: gear_curve(t * 2 * pi, 12, 2))
    .twistExtrude(gear_height, twist_angle)
    .faces(">Z")
    .workplane()
    .hole(central_hole_diameter)
)

tab = (
    cq.Workplane("XY")
    .rect(tab_width, tab_height)
    .extrude(tab_length)
    .translate((0, 0, gear_height / 2))
)

result = (
    gear_body.union(tab)
    .edges("|Z")
    .chamfer(chamfer_distance)
)
