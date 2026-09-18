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
            .lineTo(m.arm_long, 0)
            .lineTo(m.arm_long, m.thickness)
            .lineTo(m.thickness, m.thickness)
            .lineTo(m.thickness, m.arm_vertical)
            .lineTo(0, m.arm_vertical)
            .close()
            .extrude(m.width)
            .edges()
            .fillet(m.inner_fillet)
        )
        relief = (
            base
            .faces("<X")
            .workplane()
            .move(m.thickness/2, m.arm_vertical/2)
            .rect(m.relief_width, m.relief_depth)
            .cutBlind(-m.width)
        )
        holes = (
            relief
            .faces(">Z")
            .workplane()
            .move(m.holes_offset_x, m.thickness/2)
            .rect(m.hole_spacing_x, m.hole_spacing_y, forConstruction=True)
            .vertices()
            .cboreHole(m.hole_diameter, m.hole_cbore_diameter, m.hole_cbore_depth)
        )
        result = holes.edges("|Z").chamfer(m.chamfer)
        self.model = result

measures = Measures(
    arm_long=80.0,
    arm_vertical=60.0,
    thickness=8.0,
    width=30.0,
    inner_fillet=2.0,
    relief_width=15.0,
    relief_depth=20.0,
    hole_diameter=5.0,
    hole_cbore_diameter=7.5,
    hole_cbore_depth=2.0,
    hole_spacing_x=30.0,
    hole_spacing_y=30.0,
    holes_offset_x=20.0,
    chamfer=1.0,
)

result = LBracket(cq.Workplane("XY"), measures).model
