import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    width=80.0,
    depth=30.0,
    height=10.0,
    rib_height=20.0,
    rib_thickness=5.0,
    chamfer=1.0,
    hole_diameter=5.0,
    hole_spacing=40.0,
    hole_offset=15.0
)

base = (
    cq.Workplane("XY")
    .box(m.width, m.depth, m.height)
    .translate((0, 0, m.height / 2))
)

rib = (
    base.faces(">Y")
    .workplane()
    .rect(m.rib_thickness, m.rib_height)
    .extrude(m.rib_thickness)
)

combined = base.union(rib)

chamfered = combined.faces(">Z").edges().chamfer(m.chamfer)

result = (
    chamfered.faces(">Z")
    .workplane()
    .pushPoints([(-m.hole_spacing/2, 0), (m.hole_spacing/2, 0)])
    .hole(m.hole_diameter)
)
