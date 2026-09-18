import cadquery as cq
from types import SimpleNamespace as Measures

class LBracket:
    def __init__(self, workplane, measures):
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        pts = [
            (0, 0),
            (m.leg_length, 0),
            (m.leg_length, m.thickness),
            (m.thickness, m.thickness),
            (m.thickness, m.leg_height),
            (0, m.leg_height)
        ]
        base = (
            cq.Workplane('XY')
            .polyline(pts)
            .close()
            .extrude(m.thickness)
        )
        boss = (
            cq.Workplane('XY')
            .center(m.thickness/2, m.thickness/2)
            .circle(m.boss_radius)
            .extrude(m.boss_height)
        )
        model = base.union(boss)
        # Chamfer outer edges before drilling
        model = model.edges("|Z").chamfer(m.chamfer_dist)
        # Two through holes on each leg
        hole_positions = [
            (m.leg_length/2, -m.thickness/2),
            (-m.thickness/2, m.leg_height/2)
        ]
        for x, y in hole_positions:
            model = (
                model
                .faces('>Z')
                .workplane(centerOption='CenterOfBoundBox')
                .center(x, y)
                .hole(m.hole_diameter)
            )
        self.result = model

measures = Measures(
    leg_length=80.0,
    leg_height=70.0,
    thickness=10.0,
    boss_radius=8.0,
    boss_height=5.0,
    hole_diameter=6.0,
    chamfer_dist=0.5,
)

result = LBracket(cq.Workplane('XY'), measures).result
