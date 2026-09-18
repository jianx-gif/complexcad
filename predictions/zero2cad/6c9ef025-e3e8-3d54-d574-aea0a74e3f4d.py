import cadquery as cq
import math
pipe_outer_dia = 30.0
pipe_wall_thk = 4.0
pipe_inner_dia = pipe_outer_dia - 2 * pipe_wall_thk
elbow_center_radius = 40.0
elbow_angle = 60.0
flange_outer_dia = 45.0
flange_thickness = 10.0
bolt_hole_dia = 4.0
bolt_circle_radius = 15.0
fillet_radius = 1.0
outer_radius = elbow_center_radius + pipe_outer_dia / 2.0
inner_radius = elbow_center_radius - pipe_outer_dia / 2.0
profile = (
    cq.Workplane("XY")
    .moveTo(outer_radius, 0)
    .threePointArc(
        (outer_radius * math.cos(math.radians(elbow_angle / 2.0)), outer_radius * math.sin(math.radians(elbow_angle / 2.0))),
        (outer_radius * math.cos(math.radians(elbow_angle)), outer_radius * math.sin(math.radians(elbow_angle)))
    )
    .lineTo(inner_radius * math.cos(math.radians(elbow_angle)), inner_radius * math.sin(math.radians(elbow_angle)))
    .threePointArc(
        (inner_radius * math.cos(math.radians(elbow_angle / 2.0)), inner_radius * math.sin(math.radians(elbow_angle / 2.0))),
        (inner_radius, 0)
    )
    .close()
)
elbow = profile.revolve(elbow_angle)
elbow = elbow.edges().first().fillet(fillet_radius)
flange_start = (
    cq.Workplane("XZ")
    .center(outer_radius, 0)
    .circle(flange_outer_dia / 2.0)
    .extrude(flange_thickness)
)
flange_end = (
    cq.Workplane("YZ")
    .center(0, outer_radius)
    .circle(flange_outer_dia / 2.0)
    .extrude(flange_thickness)
)
result = elbow.union(flange_start).union(flange_end)
bolt_positions = [
    (bolt_circle_radius, 0),
    (0, bolt_circle_radius),
    (-bolt_circle_radius, 0),
    (0, -bolt_circle_radius)
]
result = (
    result.faces(">Y")
    .workplane()
    .pushPoints(bolt_positions)
    .hole(bolt_hole_dia)
)
result = (
    result.faces(">X")
    .workplane()
    .pushPoints(bolt_positions)
    .hole(bolt_hole_dia)
)
