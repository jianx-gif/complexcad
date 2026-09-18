import cadquery as cq
from types import SimpleNamespace as Measures

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        base = (
            cq.Workplane("XY")
            .polyline([
                (0, 0),
                (m.horizontal_length, 0),
                (m.horizontal_length, m.leg_thickness),
                (m.leg_thickness, m.leg_thickness),
                (m.leg_thickness, m.vertical_length),
                (0, m.vertical_length),
            ])
            .close()
            .extrude(m.bracket_thickness)
        )
        base = (
            base.edges()
            .filter(lambda e: abs(e.Center().x - m.leg_thickness) < 1e-3 and abs(e.Center().y - m.leg_thickness) < 1e-3)
            .fillet(m.fillet_radius)
        )
        rib = (
            cq.Workplane("XY")
            .box(m.rib_width, m.rib_thickness, m.bracket_thickness)
            .translate((m.leg_thickness + m.rib_width / 2, m.vertical_length - m.rib_thickness / 2, m.bracket_thickness / 2))
        )
        combined = base.union(rib)
        hole_positions = [
            (m.horizontal_length - m.hole_offset, m.leg_thickness / 2),
            (m.horizontal_length - m.hole_offset - m.hole_spacing, m.leg_thickness / 2),
        ]
        combined = (
            combined.faces(">Z")
            .workplane()
            .pushPoints(hole_positions)
            .hole(m.hole_diameter)
        )
        self.model = combined

measures = Measures(
    horizontal_length=70.0,
    vertical_length=80.0,
    leg_thickness=10.0,
    bracket_thickness=8.0,
    rib_width=20.0,
    rib_thickness=5.0,
    fillet_radius=3.0,
    hole_diameter=5.0,
    hole_spacing=30.0,
    hole_offset=15.0,
)

result = LBracket(cq.Workplane("XY"), measures).model