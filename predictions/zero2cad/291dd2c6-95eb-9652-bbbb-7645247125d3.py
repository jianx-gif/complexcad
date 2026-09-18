import cadquery as cq
import math

outer_diameter = 80.0
inner_diameter = 50.0
thickness = 10.0
chamfer_size = 1.0
hole_diameter = 7.0
hole_depth = 6.0
hole_count = 8
hole_radius = (inner_diameter/2 + outer_diameter/2) / 2
slot_width = 12.0
slot_height = 4.0
slot_depth = 2.0
counterbore_diameter = 10.0
counterbore_depth = 5.0
counterbore_angle = 45.0

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(thickness)
)

base = base.edges().chamfer(chamfer_size)

base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_height)
    .cutBlind(slot_depth)
)

angle_rad = math.radians(counterbore_angle)
cb_x = (outer_radius - counterbore_depth) * math.cos(angle_rad)
cb_y = (outer_radius - counterbore_depth) * math.sin(angle_rad)

base = (
    base.faces(">Z")
    .workplane()
    .center(cb_x, cb_y)
    .hole(counterbore_diameter, depth=counterbore_depth)
)

result = (
    base.faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius, startAngle=0, count=hole_count, angle=360)
    .hole(hole_diameter, depth=hole_depth)
)
