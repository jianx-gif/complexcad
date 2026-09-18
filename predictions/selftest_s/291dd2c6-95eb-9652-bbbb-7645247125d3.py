import cadquery as cq
import math

# Parameters
torus_center_radius = 30.0
pipe_thickness = 8.0
inner_radius = torus_center_radius - pipe_thickness / 2
outer_radius = torus_center_radius + pipe_thickness / 2
rib_extension = 4.0
slot_radius = 3.0
bolt_hole_dia = 5.0
counterbore_dia = 8.0
counterbore_depth = 5.0
chamfer_size = 0.8
hole_angle = 45  # degrees

# Base toroidal pipe with internal rib via revolved profile
profile = (
    cq.Workplane('XZ')
    .polyline([
        (inner_radius, -pipe_thickness/2),
        (outer_radius, -pipe_thickness/2),
        (outer_radius, pipe_thickness/2),
        (inner_radius, pipe_thickness/2),
        (inner_radius - rib_extension, pipe_thickness/2),
        (inner_radius - rib_extension, -pipe_thickness/2),
        (inner_radius, -pipe_thickness/2)
    ])
    .close()
)

base = profile.revolve().edges().chamfer(chamfer_size)

# Circular slot cut (radial cylinder)
slot_cyl = (
    cq.Workplane('XY')
    .center(torus_center_radius, 0)
    .circle(slot_radius)
    .extrude(pipe_thickness*2 + 2)
)

# Bolt through hole at specified angle
theta = math.radians(hole_angle)
hole_x = torus_center_radius * math.cos(theta)
hole_y = torus_center_radius * math.sin(theta)
through_hole = (
    cq.Workplane('XY')
    .center(hole_x, hole_y)
    .circle(bolt_hole_dia/2)
    .extrude(pipe_thickness*2 + 2)
)

# Counterbore on outer side (partial cut)
counterbore = (
    cq.Workplane('XY')
    .center(hole_x, hole_y)
    .circle(counterbore_dia/2)
    .extrude(counterbore_depth)
)

result = (
    base
    .cut(slot_cyl)
    .cut(through_hole)
    .cut(counterbore)
)
