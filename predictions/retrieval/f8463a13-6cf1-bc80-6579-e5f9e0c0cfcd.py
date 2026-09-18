import cadquery as cq
import math
from types import SimpleNamespace as Measures

outer_radius = 20.0
height = 40.0
wall_thickness = 4.0
inner_radius_top = outer_radius - wall_thickness
taper_height = 20.0
inner_radius_bottom = inner_radius_top - 2.0
bore_radius = 3.0
blind_depth = 30.0
chamfer_length = 2.0
chamfer_angle_deg = 30.0
chamfer_length2 = chamfer_length * math.tan(math.radians(chamfer_angle_deg))

# Outer solid
outer_profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (outer_radius, 0),
        (outer_radius, height),
        (0, height),
    ])
    .close()
)
outer_solid = outer_profile.revolve()

# Inner cavity profile (including axis)
inner_profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (inner_radius_top, 0),
        (inner_radius_bottom, taper_height),
        (inner_radius_bottom, height),
        (0, height),
    ])
    .close()
)
inner_cavity = inner_profile.revolve()

socket_body = outer_solid.cut(inner_cavity)

# Blind bore cut (does not go through)
blind_bore = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(bore_radius)
    .extrude(blind_depth)
)
socket_body = socket_body.cut(blind_bore)

# Chamfer on the top opening edge
socket_body = socket_body.edges(">Z").chamfer(chamfer_length, chamfer_length2)

result = socket_body
