import cadquery as cq
from types import SimpleNamespace as Measures

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        vertical = (
            cq.Workplane("XY")
            .box(m.arm_width, m.vertical_arm_length, m.sheet_thickness, centered=(True, False, False))
            .translate((-m.arm_width/2, 0, 0))
        )
        horizontal = (
            cq.Workplane("XY")
            .box(m.horizontal_arm_length, m.arm_width, m.sheet_thickness, centered=(False, True, False))
            .translate((0, m.arm_width/2, 0))
        )
        base = vertical.union(horizontal)
        rounded = (
            cq.Workplane("XY")
            .center(m.arm_width, m.arm_width)
            .circle(m.fillet_radius)
            .extrude(m.sheet_thickness*2)
        )
        base = base.cut(rounded)
        rib = (
            base.faces(">Z").workplane()
            .polyline([
                (0, 0),
                (m.rib_height, 0),
                (0, m.rib_height)
            ])
            .close()
            .extrude(m.rib_thickness)
        )
        solid = base.union(rib)
        # Position the first hole column offset from inner side
        solid = (
            solid.faces(">Z").workplane()
            .moveTo(m.column_offset, m.edge_distance)
            .rarray(m.col_spacing, m.row_spacing, 2, m.rows)
            .hole(m.hole_diameter)
        )
        self.model = solid

measures = Measures(
    horizontal_arm_length=80.0,
    vertical_arm_length=60.0,
    arm_width=30.0,
    sheet_thickness=5.0,
    fillet_radius=10.0,
    rib_height=15.0,
    rib_thickness=2.0,
    hole_diameter=5.0,
    column_offset=5.0,
    edge_distance=5.0,
    rows=5,
    col_spacing=20.0,
    row_spacing=12.5,
)

result = LBracket(cq.Workplane("XY"), measures).model
