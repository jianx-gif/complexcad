import cadquery as cq
from types import SimpleNamespace as Measures

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        wp = cq.Workplane("XY")
        profile = (
            wp
            .moveTo(0, 0)
            .lineTo(m.long_leg, 0)
            .lineTo(m.long_leg, m.leg_width)
            .lineTo(m.leg_width + m.inner_radius, m.leg_width)
            .threePointArc((m.leg_width, m.leg_width), (m.leg_width, m.leg_width + m.inner_radius))
            .lineTo(m.leg_width, m.short_leg)
            .lineTo(0, m.short_leg)
            .close()
        )
        solid = profile.extrude(m.wall_thickness)
        # Add mounting holes on long leg
        holes_long = (
            solid.faces("<Z")
            .workplane()
            .pushPoints([
                (m.long_leg/2, m.leg_width/2),
                (m.long_leg/2, m.leg_width/2 + m.hole_spacing_long)
            ])
            .hole(m.hole_diameter)
        )
        # Add mounting holes on short leg
        result = (
            holes_long.faces("<Z")
            .workplane()
            .pushPoints([
                (m.leg_width/2, m.short_leg/2),
                (m.leg_width/2 + m.hole_spacing_short, m.short_leg/2)
            ])
            .hole(m.hole_diameter)
        )
        # Add small chamfer to outer edges for safety
        result = result.edges("|Z").chamfer(m.chamfer_size)
        self.model = result

cq.Workplane.part = lambda self, part_class, measures: part_class(self, measures).model

measures = Measures(
    long_leg=80.0,
    short_leg=60.0,
    leg_width=20.0,
    wall_thickness=2.0,
    inner_radius=10.0,
    hole_diameter=5.0,
    hole_spacing_long=15.0,
    hole_spacing_short=15.0,
    chamfer_size=0.5,
)

result = cq.Workplane("XY").part(LBracket, measures)
