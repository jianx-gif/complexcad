import cadquery as cq
import math

outer_d = 60.0
length_body = 80.0
wall_t = 2.5
fillet_r = 5.0
edge_fillet = 1.0
inlet_r = 8.0
outlet_r = 10.0
flange_extra = 15.0
flange_thk = 5.0
bolt_hole_r = 2.0
bolt_pattern_radius = outer_d/2 + flange_extra - 5.0

outer = (
    cq.Workplane('XY')
    .circle(outer_d/2)
    .extrude(length_body)
)
body = outer.shell(-wall_t)
body = body.faces('>Z').edges().fillet(fillet_r)
body = body.faces('<Z').edges().fillet(fillet_r)
body = body.edges().fillet(edge_fillet)

inlet = (
    cq.Workplane('YZ')
    .workplane(offset=-(outer_d/2 + inlet_r))
    .center(0, length_body*0.25)
    .circle(inlet_r)
    .extrude(outer_d + 2*inlet_r)
)
outlet = (
    cq.Workplane('YZ')
    .workplane(offset=outer_d/2 + outlet_r)
    .center(0, length_body*0.75)
    .circle(outlet_r)
    .extrude(outer_d + 2*outlet_r)
)
body = body.cut(inlet)
body = body.cut(outlet)

flange = (
    cq.Workplane('XY')
    .circle((outer_d/2) + flange_extra)
    .extrude(flange_thk)
    .translate((0, 0, -flange_thk))
)
body = body.union(flange)

for a in range(0, 360, 90):
    x = bolt_pattern_radius * math.cos(math.radians(a))
    y = bolt_pattern_radius * math.sin(math.radians(a))
    hole = (
        cq.Workplane('XY')
        .center(x, y)
        .circle(bolt_hole_r)
        .extrude(- (flange_thk + wall_t))
    )
    body = body.cut(hole)

result = body
