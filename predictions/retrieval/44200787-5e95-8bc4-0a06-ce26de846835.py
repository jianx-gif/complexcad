
import cadquery as cq

class LBracketMeasures:
    def __init__(self):
        self.long_leg = 80.0
        self.short_leg = 50.0
        self.leg_thick = 10.0
        self.wall_thick = 4.0
        self.depth = 15.0
        self.fillet = 2.0
        self.hole_dia = 5.0
        self.hole_spacing = 30.0
        self.hole_offset = 12.0

class LBracket:
    def __init__(self, workplane, measures):
        self.wp = workplane
        self.m = measures
        self.model = self.build()

    def build(self):
        m = self.m
        pts = [
            (0, 0),
            (m.long_leg, 0),
            (m.long_leg, m.leg_thick),
            (m.leg_thick, m.leg_thick),
            (m.leg_thick, m.short_leg),
            (0, m.short_leg),
            (0, 0)
        ]
        solid = (
            cq.Workplane('XY')
            .polyline(pts)
            .close()
            .workplane(offset=m.depth)
            .polyline(pts)
            .close()
            .offset2D(m.wall_thick)
            .loft(combine=True)
        )
        solid = solid.edges().fillet(m.fillet)
        solid = (
            solid.faces('>Y')
            .workplane(centerOption='CenterOfBoundBox')
            .center(m.hole_offset, m.short_leg/2)
            .hole(m.hole_dia)
            .center(0, m.hole_spacing)
            .hole(m.hole_dia)
        )
        return solid

measures = LBracketMeasures()
result = LBracket(cq.Workplane('XY'), measures).model
