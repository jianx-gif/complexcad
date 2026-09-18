import cadquery as cq
from math import acos, degrees

# Primary dimensions
linear_width = 70.0
depth = 12.0
height = 20.0
tab_height = 5.0
arc_outer_diameter = 100.0
slot_width = 2.5
slot_length = 8.0
slot_count = 4
chamfer_distance = 0.5

# Derived geometry
arc_outer_radius = 0.5 * arc_outer_diameter
arc_center_diameter = arc_outer_diameter - depth
arc_center_radius = 0.5 * arc_center_diameter
arc_center_angle = degrees(acos((2 * arc_center_radius**2 - linear_width**2) / (2 * arc_center_radius**2)))
arc_secant_angle = 0.5 * (180 - arc_center_angle)

# Path for sweep (arc in XY plane)
path = (
    cq.Workplane("XY")
    .radiusArc((linear_width, 0.0), arc_center_radius)
    .wire()
)

result = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -arc_secant_angle, 0))
    .polyline([
        (0, 0),
        (depth, 0),
        (depth, height),
        (depth / 2, height + tab_height),
        (0, height),
    ])
    .close()
    .sweep(path, transition="round")
    .edges("|Z")
    .chamfer(chamfer_distance)
    .faces(">Z")
    .workplane()
    .rarray(linear_width / (slot_count + 1), 0, slot_count, 1)
    .rect(slot_width, slot_length)
    .cutBlind(-depth)
)
