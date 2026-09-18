import cadquery as cq
import math

pipe_outer_diameter = 20.0
wall_thickness = 2.0
pipe_radius = pipe_outer_diameter / 2.0
bend_radius = 30.0
bend_angle = 45.0
outer_arc_radius = bend_radius + pipe_radius
inner_arc_radius = bend_radius - pipe_radius
keyway_width = 4.0
keyway_depth = 3.0
keyway_length = bend_radius * 2.0
tapped_hole_diameter = 5.0
tapped_hole_depth = wall_thickness + 5.0
chamfer_size = 0.5

profile = (
    cq.Workplane('XY')
    .moveTo(outer_arc_radius, 0)
    .threePointArc(
        (outer_arc_radius * math.cos(math.radians(bend_angle/2.0)),
         outer_arc_radius * math.sin(math.radians(bend_angle/2.0))),
        (outer_arc_radius * math.cos(math.radians(bend_angle)),
         outer_arc_radius * math.sin(math.radians(bend_angle)))
    )
    .lineTo(
        inner_arc_radius * math.cos(math.radians(bend_angle)),
        inner_arc_radius * math.sin(math.radians(bend_angle))
    )
    .threePointArc(
        (inner_arc_radius * math.cos(math.radians(bend_angle/2.0)),
         inner_arc_radius * math.sin(math.radians(bend_angle/2.0))),
        (inner_arc_radius, 0)
    )
    .close()
)

result = profile.revolve(180)

mid_angle = bend_angle / 2.0
center_x = bend_radius * math.cos(math.radians(mid_angle))
center_y = bend_radius * math.sin(math.radians(mid_angle))

keyway_box = (
    cq.Workplane('XY')
    .box(keyway_length, keyway_width, keyway_depth)
    .translate((center_x, center_y, 0))
    .rotate((0, 0, 0), (0, 0, 1), mid_angle + 90.0)
)

result = result.cut(keyway_box)

hole_center_x = bend_radius + pipe_radius
hole = (
    cq.Workplane('XY')
    .center(hole_center_x, 0)
    .circle(tapped_hole_diameter / 2.0)
    .extrude(tapped_hole_depth)
    .rotate((0, 0, 0), (1, 0, 0), -90.0)
)

result = result.cut(hole)

result = result.edges().chamfer(chamfer_size)
