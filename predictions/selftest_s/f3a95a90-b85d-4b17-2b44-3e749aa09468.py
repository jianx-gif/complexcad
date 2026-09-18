import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    plate_width=80.0, plate_depth=30.0, plate_thickness=6.0,
    boss_width=30.0, boss_depth=15.0, boss_height=5.0,
    fillet_radius=2.0, chamfer_distance=0.8,
    pocket_width=40.0, pocket_depth=20.0, pocket_thickness=3.0,
    hole1=Measures(x_offset=-10.0, diameter=3.0, cs_diameter=6.0, cs_angle=90.0, depth=4.0),
    hole2=Measures(x_offset=10.0, diameter=3.0, cs_diameter=6.0, cs_angle=90.0, depth=4.0)
)
result = (
    cq.Workplane('XY')
    .rect(m.plate_width, m.plate_depth)
    .extrude(m.plate_thickness)
    .faces('<Z')
    .workplane()
    .rect(m.pocket_width, m.pocket_depth)
    .cutBlind(m.pocket_thickness)
    .faces('>Z')
    .workplane()
    .rect(m.boss_width, m.boss_depth)
    .extrude(m.boss_height)
    .faces('>Z')
    .edges()
    .fillet(m.fillet_radius)
    .faces('>Z')
    .workplane()
    .pushPoints([(m.hole1.x_offset,0),(m.hole2.x_offset,0)])
    .cskHole(m.hole1.diameter, m.hole1.cs_diameter, m.hole1.cs_angle, m.hole1.depth)
)
