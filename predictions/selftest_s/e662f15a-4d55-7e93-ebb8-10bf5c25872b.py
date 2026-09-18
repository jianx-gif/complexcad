import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    width=80.0,
    depth=40.0,
    height=15.0,
    wall_thickness=3.0,
    hinge_radius=6.0,
    hinge_depth=5.0,
    cbore_clearance=9.0,
    cbore_diameter=6.0,
    cbore_depth=4.0,
    fillet_radius=2.0,
    rib_thickness=2.0,
    rib_height=10.0,
    rib_spacing=12.0,
    rib_count=3
)

base = (
    cq.Workplane('XY')
    .sketch()
    .rect(m.width, m.depth)
    .finalize()
    .extrude(m.height)
)

base = base.faces('>Z').edges().fillet(m.fillet_radius)

base = (
    base.faces('>X')
    .workplane()
    .center(m.width/2 - m.wall_thickness/2, 0)
    .cboreHole(m.cbore_clearance, m.cbore_diameter, m.cbore_depth)
)

for i in range(m.rib_count):
    offset = -m.width/2 + m.rib_spacing * (i + 1)
    base = (
        base.faces('<X')
        .workplane()
        .center(offset, 0)
        .rect(m.rib_thickness, m.rib_height)
        .cutBlind(-m.rib_thickness)
    )

pivot = (
    base.faces('>Z')
    .workplane()
    .center(0, 0)
    .circle(m.hinge_radius)
    .cutBlind(-m.hinge_depth)
)

result = pivot