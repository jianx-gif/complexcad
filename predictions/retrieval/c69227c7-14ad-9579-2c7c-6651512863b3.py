import cadquery as cq
from types import SimpleNamespace as Measures

outer_dia = 30.0
height = 20.0
flange_dia = 40.0
flange_thickness = 3.0
thread_dia = 6.0
chamfer_size = 1.0
rib_count = 4
rib_width = 2.0
rib_height = 6.0
rib_thickness = 0.5

base = (
    cq.Workplane('XY')
    .circle(outer_dia / 2)
    .extrude(height)
)

flange = (
    cq.Workplane('XY')
    .circle(flange_dia / 2)
    .extrude(flange_thickness)
)

body = base.union(flange.translate((0, 0, -flange_thickness)))

hole = (
    cq.Workplane('XY')
    .circle(thread_dia / 2)
    .extrude(height + flange_thickness)
)

body = body.cut(hole)

body = body.edges('>Z').chamfer(chamfer_size)

ribs = []
angle_step = 360 / rib_count
for i in range(rib_count):
    rib = (
        cq.Workplane('XZ')
        .rect(rib_width, rib_height)
        .extrude(rib_thickness)
        .translate((0, outer_dia/2 - rib_thickness/2, height/2))
        .rotate((0,0,0), (0,0,1), i * angle_step)
    )
    ribs.append(rib)

for rib in ribs:
    body = body.union(rib)

result = body