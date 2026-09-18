import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    outer_radius=45.0,
    inner_radius=30.0,
    thickness=8.0,
    groove_width=2.0,
    groove_depth=1.5,
    chamfer=0.8,
    hole_diameter=4.5,
    hole_depth=5.0,
    hole_count=4,
    hole_radius=38.0
)

profile = (
    cq.Workplane("XZ")
    .moveTo(m.inner_radius, 0)
    .lineTo(m.inner_radius, m.thickness)
    .lineTo(m.outer_radius, m.thickness)
    .lineTo(m.outer_radius, 0)
    .close()
)

ring = profile.revolve()

ring = ring.faces(">Z").edges().chamfer(m.chamfer)

ring = (
    ring.faces(">Z")
    .workplane()
    .circle(m.inner_radius - m.groove_width/2)
    .cutBlind(m.groove_depth)
)

ring = (
    ring.faces(">Z")
    .workplane()
    .polarArray(radius=m.hole_radius, startAngle=0, angle=360, count=m.hole_count)
    .hole(m.hole_diameter, depth=m.hole_depth)
)

result = ring