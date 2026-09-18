import cadquery as cq
from dataclasses import dataclass

@dataclass
class Measures:
    leg_length_long: float
    leg_length_short: float
    leg_thickness: float
    leg_width: float
    boss_radius: float
    boss_height: float
    countersink_diameter: float
    countersink_top_diameter: float
    countersink_angle: float
    chamfer_distance: float
    rib_thickness: float
    rib_spacing: float
    gusset_thickness: float
    gusset_enabled: bool

class LBracketWithBoss:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        long_leg = (
            cq.Workplane('XY')
            .box(m.leg_width, m.leg_thickness, m.leg_length_long)
            .translate((0, -m.leg_thickness/2, m.leg_length_long/2))
        )
        short_leg = (
            cq.Workplane('XY')
            .box(m.leg_width, m.leg_thickness, m.leg_length_short)
            .translate((0, -m.leg_thickness/2, -m.leg_length_short/2))
        )
        l_shape = long_leg.union(short_leg)
        rib = (
            cq.Workplane('XY')
            .box(m.rib_thickness, m.leg_thickness, m.rib_spacing)
            .translate((m.leg_width/2 - m.rib_thickness/2, 0, 0))
        )
        ribs = rib
        count = int(m.leg_length_long // m.rib_spacing)
        for i in range(1, count):
            ribs = ribs.union(rib.translate((0, 0, i*m.rib_spacing)))
        l_shape = l_shape.union(ribs)
        l_shape = l_shape.edges().chamfer(m.chamfer_distance)
        boss_profile = (
            cq.Workplane('XZ')
            .moveTo(0, 0)
            .lineTo(m.boss_radius, 0)
            .lineTo(m.boss_radius, m.boss_height)
            .lineTo(0, m.boss_height)
            .close()
        )
        boss = boss_profile.revolve(360, (0,0,0), (0,1,0))
        l_shape = l_shape.union(boss)
        l_shape = (
            l_shape.faces('>Y')
            .workplane(centerOption='CenterOfBoundBox')
            .cskHole(m.countersink_diameter, m.countersink_top_diameter, m.countersink_angle, depth=m.boss_height)
        )
        if m.gusset_enabled:
            gusset = (
                cq.Workplane('XY')
                .polyline([
                    (0,0),
                    (m.gusset_thickness,0),
                    (0,m.gusset_thickness)
                ])
                .close()
                .extrude(m.leg_width)
                .translate((0, -m.leg_thickness/2, 0))
            )
            l_shape = l_shape.union(gusset)
        self.model = l_shape

measures = Measures(
    leg_length_long=80.0,
    leg_length_short=60.0,
    leg_thickness=8.0,
    leg_width=12.0,
    boss_radius=10.0,
    boss_height=30.0,
    countersink_diameter=6.0,
    countersink_top_diameter=12.0,
    countersink_angle=82.0,
    chamfer_distance=1.0,
    rib_thickness=4.0,
    rib_spacing=20.0,
    gusset_thickness=5.0,
    gusset_enabled=True
)

result = LBracketWithBoss(cq.Workplane('XY'), measures).model