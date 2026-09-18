import cadquery as cq
from types import SimpleNamespace as Measures

leg_length_long = 80.0
leg_length_short = 50.0
leg_thickness = 10.0
leg_width = 20.0
chamfer_distance = 1.0
clearance_hole_diameter = 5.0
hole_margin = 4.0
gusset_thickness = 5.0

hole_spacing = (leg_width - 2 * hole_margin) / (5 - 1)
inner_corner_x = leg_length_long / 2 - leg_thickness / 2

long_leg = (
    cq.Workplane("XY")
    .box(leg_length_long, leg_thickness, leg_width)
)

short_leg = (
    cq.Workplane("XY")
    .box(leg_thickness, leg_length_short, leg_width)
    .translate((inner_corner_x, leg_length_short / 2, 0))
)

hole_positions = [(0, hole_margin + i * hole_spacing) for i in range(5)]
short_leg = (
    short_leg
    .faces("+Y")
    .workplane()
    .pushPoints(hole_positions)
    .hole(clearance_hole_diameter)
)

base_bracket = long_leg.union(short_leg)

gusset = (
    cq.Workplane("YZ")
    .polyline([(0, 0), (0, leg_width), (gusset_thickness, 0)])
    .close()
    .extrude(gusset_thickness)
    .translate((inner_corner_x, 0, 0))
)

result = (
    base_bracket.union(gusset)
    .edges()
    .chamfer(chamfer_distance)
)
