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
                (m.horizontal_leg_length, 0),
                (m.horizontal_leg_length, m.leg_thickness),
                (m.leg_thickness, m.leg_thickness),
                (m.leg_thickness, m.vertical_leg_length),
                (0, m.vertical_leg_length),
            ])
            .close()
            .extrude(m.bracket_thickness)
        )
        rib = (
            base.faces(">X")
            .workplane(centerOption="CenterOfBoundBox")
            .rect(m.rib_width, m.rib_height)
            .extrude(m.rib_thickness)
        )
        combined = base.union(rib)
        holes = (
            combined.faces(">Z")
            .workplane()
            .move(m.horizontal_leg_length - m.hole_offset_from_end, m.leg_thickness / 2)
            .rarray(m.hole_spacing, 0, 2, 1)
            .hole(m.hole_diameter)
        )
        result = (
            holes.faces(">Z")
            .edges()
            .chamfer(m.chamfer_distance)
        )
        self.model = result

measures = Measures(
    horizontal_leg_length=60.0,
    vertical_leg_length=80.0,
    leg_thickness=10.0,
    bracket_thickness=8.0,
    rib_width=5.0,
    rib_height=6.0,
    rib_thickness=3.0,
    hole_diameter=4.5,
    hole_spacing=30.0,
    hole_offset_from_end=15.0,
    chamfer_distance=0.8,
)

result = LBracket(cq.Workplane("XY"), measures).model