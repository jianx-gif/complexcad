import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    outer_radius=45.0,
    inner_radius=30.0,
    thickness=10.0,
    sector_angle=120.0,
    chamfer=0.8,
    hole_diameter=4.0,
    hole_depth=6.0,
    hole_count=4,
    hole_radius_offset=32.0,
)

profile = (
    cq.Workplane("XZ")
    .moveTo(m.inner_radius, 0)
    .lineTo(m.outer_radius, 0)
    .lineTo(m.outer_radius, m.thickness)
    .lineTo(m.inner_radius, m.thickness)
    .close()
)

result = (
    profile
    .revolve(m.sector_angle)
    .edges("|Z")
    .chamfer(m.chamfer)
    .faces(">Z")
    .workplane()
    .polarArray(radius=m.hole_radius_offset, startAngle=0, count=m.hole_count, angle=m.sector_angle)
    .hole(m.hole_diameter, depth=m.hole_depth)
)
