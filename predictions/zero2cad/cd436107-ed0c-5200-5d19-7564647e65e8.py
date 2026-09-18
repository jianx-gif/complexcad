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
                (m.horizontal_length, m.thickness),
                (m.thickness, m.thickness),
                (m.thickness, m.vertical_length),
                (0, m.vertical_length),
            ])
            .close()
            .extrude(m.thickness)
        )
        rib = (
            cq.Workplane("XY")
            .rect(m.rib_width, m.rib_height)
            .translate((m.thickness, m.thickness, 0))
            .extrude(m.thickness)
        )
        combined = base.union(rib)
        with_hole = (
            combined.faces(">Z")
            .workplane()
            .center(m.horizontal_length / 2, m.thickness / 2)
            .hole(m.hole_diameter)
        )
        self.model = with_hole

measures = Measures(
    horizontal_length=70.0,
    vertical_length=50.0,
    thickness=8.0,
    rib_width=12.0,
    rib_height=25.0,
    hole_diameter=6.5,
)

result = LBracket(cq.Workplane("XY"), measures).model