import cadquery as cq
from types import SimpleNamespace as Measures

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        # Base L profile
        base = (
            cq.Workplane("XY")
            .polyline([
                (0, 0),
                (m.horizontal_length, 0),
                (m.horizontal_length, m.thickness),
                (m.thickness, m.thickness),
                (m.thickness, m.vertical_length),
                (0, m.vertical_length),
                (0, 0),
            ])
            .close()
            .extrude(m.width)
        )
        # Notch on horizontal leg
        notch = (
            cq.Workplane("XY")
            .center(m.horizontal_length/2, m.thickness/2)
            .rect(m.notch_width, m.notch_depth)
            .extrude(m.width)
        )
        base = base.cut(notch)
        # Chamfer outer edges
        base = base.edges().chamfer(m.chamfer)
        # Mounting holes on horizontal leg
        horiz_hole_pts = [
            (m.horizontal_length/2 - m.hole_spacing/2, m.thickness/2),
            (m.horizontal_length/2 + m.hole_spacing/2, m.thickness/2),
        ]
        # Mounting holes on vertical leg
        vert_hole_pts = [
            (m.thickness/2, m.vertical_length/2 - m.hole_spacing/2),
            (m.thickness/2, m.vertical_length/2 + m.hole_spacing/2),
        ]
        # Drill holes through top face
        base = (
            base.faces(">Z")
            .workplane()
            .pushPoints(horiz_hole_pts)
            .hole(m.hole_diameter)
            .pushPoints(vert_hole_pts)
            .hole(m.hole_diameter)
        )
        # Blind tapped hole on inner vertical face
        base = (
            base.faces("<X")
            .workplane()
            .center(m.thickness/2, m.vertical_length/2)
            .hole(m.blind_hole_diameter, depth=m.blind_hole_depth)
        )
        self.model = base

measures = Measures(
    horizontal_length=80.0,
    vertical_length=70.0,
    thickness=6.0,
    width=12.0,
    notch_width=20.0,
    notch_depth=4.0,
    chamfer=0.5,
    hole_diameter=5.0,
    hole_spacing=25.0,
    blind_hole_diameter=6.0,
    blind_hole_depth=8.0,
)

result = LBracket(cq.Workplane("XY"), measures).model