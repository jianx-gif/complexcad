import cadquery as cq
from types import SimpleNamespace as Measures

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        outer = (
            cq.Workplane("XY")
            .rect(m.outer_width, m.outer_height)
            .extrude(m.thickness)
        )
        inner = (
            cq.Workplane("XY")
            .rect(m.inner_width, m.inner_height)
            .translate((m.thickness, m.thickness))
            .extrude(m.thickness)
        )
        base = outer.cut(inner)
        base = base.edges(">X or <X or >Y or <Y").chamfer(m.chamfer)
        base = (
            base.faces(">X")
            .workplane(centerOption="CenterOfBoundBox")
            .cskHole(m.screw_diameter, m.countersink_diameter, m.countersink_angle, m.thickness)
        )
        base = (
            base.faces(">Z")
            .workplane(centerOption="CenterOfBoundBox")
            .rarray(m.hole_spacing, 0, m.hole_count, 1)
            .hole(m.hole_diameter)
        )
        self.model = base

measures = Measures(
    outer_width=80.0,
    outer_height=100.0,
    thickness=15.0,
    inner_width=60.0,
    inner_height=80.0,
    chamfer=1.0,
    screw_diameter=4.0,
    countersink_diameter=8.0,
    countersink_angle=90.0,
    hole_diameter=5.0,
    hole_spacing=20.0,
    hole_count=4,
)

result = LBracket(cq.Workplane("XY"), measures).model