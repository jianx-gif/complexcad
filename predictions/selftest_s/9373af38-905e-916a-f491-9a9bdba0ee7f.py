import cadquery as cq
import math
centerline_radius = 30.0
pipe_outer_diameter = 20.0
pipe_wall_thickness = 2.0
pipe_outer_radius = pipe_outer_diameter / 2.0
fillet_radius = 2.0
insert_diameter = 6.0
insert_length = 12.0
angles = [0, 30, 60, 90]
path = cq.Workplane("XZ").moveTo(0, 0).threePointArc((centerline_radius, 0), (centerline_radius, centerline_radius)).wire()
profile = cq.Workplane("XY").circle(pipe_outer_radius)
elbow_outer = profile.sweep(path)
elbow = elbow_outer.shell(-pipe_wall_thickness)
elbow = elbow.edges().filter(lambda e: e.geomType() == "CIRCLE").fillet(fillet_radius)
for angle in angles:
    rad = math.radians(angle)
    x = (centerline_radius + pipe_outer_radius) * math.cos(rad)
    z = (centerline_radius + pipe_outer_radius) * math.sin(rad)
    hole = (
        cq.Workplane("XZ")
        .transformed(offset=(x, 0, z), rotate=(0, -angle, 0))
        .circle(insert_diameter / 2.0)
        .extrude(-insert_length)
    )
    elbow = elbow.cut(hole)
result = elbow