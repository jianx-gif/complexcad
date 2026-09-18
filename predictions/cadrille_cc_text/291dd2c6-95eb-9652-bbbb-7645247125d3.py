import cadquery as cq
import math
from types import SimpleNamespace as Measures
m = Measures(
    toroth_center_radius=30.0,
    pipe_thickness=8.0,
    bolt_hole_dia=5.0,
    counterbore_dia=8.0,
    counterbore_depth=5.0,
    chamfer_size=0.8,
    hole_angle=45.0,
    hole_count=4,
)
m.arc_angle_rad = math.radians(m.arc_angle_rad)
m.arc_center_radius = 0.5 * m.arc_angle_rad
m.arc_center_radius = 0.5 * m.arc_center_radius
m.arc_center_angle = 0.5 * m.arc_angle_rad
m.arc_center_radius = 0.5 * m.arc_center_radius
m.arc_center_angle = 0.5 * m.arc_center_radius
m.arc_center_radius = 0.5 * m.arc_center_radius
m.arc_angle = 0.5 * m.arc_center_radius
m.arc_center_radius = 0.5 * m.arc_center_radius
m.arc_center_angle = 0.5 * m.arc_center_radius
m.arc_center_radius = 0.5 * m.arc_center_radius
m.arc_center_radius = 0.5 * m.arc_center_radius
m.arc_center_angle = 0.5 * m.arc_center_radius
m.arc_center_radius = 0.5 * m.arc_center_radius
m.arc_center_radius = 0.5 * m.arc_center_radius
m.arc_center_angle = 0.5 * m.arc_center_radius
m.arc_center_radius = 0.5 * m.arc_center_radius
m.arc_center_radius = 0.5 * m.arc_center_radius
m.arc_angle = 0.5 * (180 - m.arc_center_angle)
m.arc_center_radius = 0.5 * m.arc_center_radius
m.arc_center_angle = 0.5 * (180 - m.arc_center_radius)
path = (
    cq.Workplane("XZ")
    .polyline(m.arc_center_radius, m.arc_center_radius, m.arc_center_radius)
    .close()
)
result = (
    cq.Workplane("XY")
    .circle(m.arc_center_radius)
    .extrude(m.arc_center_radius)
)
result = result.cut(m.arc_center_radius)
result = result.edges().chamfer(m.chamfer_size)
result = result.edges().chamfer(m.chamfer_size)
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(m.hole_angle, m.hole_count, m.hole_angle)
    .hole(m.hole_dia)
)
