import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    outer_radius=30.0,
    inner_radius=20.0,
    thickness=5.0,
    socket_depth=2.0,
    pocket_width=8.0,
    pocket_depth=2.0,
    chamfer=0.5,
    hole_diameter=3.0,
    hole_depth=2.5,
    hole_radial_offset=25.0
)

profile = (
    cq.Workplane('XZ')
    .moveTo(m.inner_radius, 0)
    .lineTo(m.inner_radius, m.thickness)
    .lineTo(m.outer_radius, m.thickness)
    .lineTo(m.outer_radius, 0)
    .close()
)

ring = profile.revolve(360)

central_socket = (
    cq.Workplane('XY')
    .circle(m.inner_radius - 0.5)
    .extrude(-m.socket_depth)
)

side_pocket = (
    cq.Workplane('XY')
    .center(m.outer_radius, 0)
    .rect(m.pocket_width, m.thickness)
    .extrude(-m.pocket_depth)
)

result = (
    ring
    .cut(central_socket)
    .cut(side_pocket)
    .edges('>Z').chamfer(m.chamfer)
)

result = (
    result
    .faces('>Z').workplane()
    .polarArray(count=4, radius=m.hole_radial_offset, startAngle=0, angle=360)
    .hole(m.hole_diameter, depth=m.hole_depth)
)
