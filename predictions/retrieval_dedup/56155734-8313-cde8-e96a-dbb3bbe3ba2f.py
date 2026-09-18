import cadquery as cq
from types import SimpleNamespace as Measures
from math import cos, sin, radians

p = Measures(
    block_width=45.0,
    block_depth=15.0,
    block_height=12.0,
    arc_radius=30.0,
    arc_angle=120.0,
    fillet_radius=3.0,
    boss_diameter=8.0,
    boss_height=10.0,
    tap_diameter=5.0,
    pocket_diameter=6.0,
    pocket_offset=10.0
)

p.arc_angle_rad = radians(p.arc_angle)
# secant angle for orientation of sweep profile
p.arc_secant_angle = (180.0 - p.arc_angle) / 2.0

# Sweep path along 120-degree arc
path = (
    cq.Workplane('XY')
    .radiusArc((p.block_width, 0), p.arc_radius)
    .wire()
)

# Sweep base rectangular profile with depth and height
swept = (
    cq.Workplane('XY')
    .transformed(rotate=(90, -p.arc_secant_angle, 0))
    .rect(p.block_depth, p.block_height)
    .sweep(path, transition='round')
)

# Add pocket cut, fillet, boss, and tapped hole
result = (
    swept
    .faces('>Z')
    .workplane()
    .center(p.pocket_offset, 0)
    .circle(p.pocket_diameter/2)
    .cutBlind(p.block_height/2)
    .edges('|Z')
    .fillet(p.fillet_radius)
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .circle(p.boss_diameter/2)
    .extrude(p.boss_height)
    .faces('>Z')
    .workplane()
    .hole(p.tap_diameter, depth=p.boss_height)
)
