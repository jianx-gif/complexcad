import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    width = 60.0,
    height = 30.0,
    thickness = 15.0,
    arc_radius = 12.0,
    chamfer = 1.5,
    hole_diameter = 4.0,
    hole_spacing = 20.0,
    hole_offset_y = 8.0
)

profile = (
    cq.Workplane("XY")
    .moveTo(-m.width/2, 0)
    .lineTo(m.width/2, 0)
    .lineTo(m.width/2 - m.arc_radius, m.height)
    .lineTo(-m.width/2 + m.arc_radius, m.height)
    .close()
)

solid = (
    profile
    .extrude(m.thickness)
    .faces(">Z")
    .workplane()
    .center(0, m.height/2)
    .circle(m.arc_radius)
    .cutBlind(-m.thickness)
    .edges()
    .chamfer(m.chamfer)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-m.hole_spacing/2, m.hole_offset_y),
        (m.hole_spacing/2, m.hole_offset_y)
    ])
    .hole(m.hole_diameter)
)

result = solid
