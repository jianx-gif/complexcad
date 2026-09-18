import cadquery as cq
import math

outer_radius = 20.0
knob_height = 30.0
knurl_width = 2.0
knurl_depth = 2.0
num_knrows = 24
central_hole_radius = 5.0
central_hole_depth = knob_height - 4.0
top_chamfer = 1.0
slot_width = 6.0
slot_depth = 4.0
slot_height = 8.0

base = (
    cq.Workplane('XY')
    .circle(outer_radius)
    .extrude(knob_height)
    .faces('>Z')
    .workplane()
    .tag('knob_top')
)

slot = (
    cq.Workplane('XY')
    .center(0, outer_radius - slot_depth/2)
    .rect(slot_width, slot_depth)
    .extrude(-slot_height)
)

result = base.cut(slot.val())

points = []
radius = outer_radius - knurl_depth/2
for i in range(num_knrows):
    angle = 2*math.pi*i/num_knrows
    x = radius*math.cos(angle)
    y = radius*math.sin(angle)
    points.append((x, y))

knurl = (
    cq.Workplane('XY')
    .pushPoints(points)
    .circle(knurl_width/2)
    .extrude(knob_height)
)

result = result.union(knurl.val())

result = (
    result.faces('>Z')
    .workplane()
    .hole(central_hole_radius*2, central_hole_depth)
)

result = result.edges('>Z').chamfer(top_chamfer)

result