import cadquery as cq
from types import SimpleNamespace as Measures

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()
    def build(self):
        m = self.measures
        # L profile sketch and extrusion
        solid = (
            cq.Workplane('XY')
            .polyline([
                (0, 0),
                (m.horizontal_leg_length, 0),
                (m.horizontal_leg_length, m.leg_thickness),
                (m.leg_thickness, m.leg_thickness),
                (m.leg_thickness, m.vertical_leg_height),
                (0, m.vertical_leg_height),
            ])
            .close()
            .extrude(m.bracket_thickness)
        )
        # fillet the interior corner edge (inner bend)
        inner_edges = solid.edges('|Z').filter(
            lambda e: abs(e.Center().x - m.leg_thickness) < 0.01 and abs(e.Center().y - m.leg_thickness) < 0.01
        )
        solid = inner_edges.fillet(m.inner_fillet_radius)
        # through holes on vertical leg front face
        start_y = m.hole_edge_distance + m.hole_diameter / 2.0
        start_x = m.hole_edge_distance + m.hole_diameter / 2.0
        hole_positions = [(start_x, start_y + i * m.hole_spacing) for i in range(m.hole_count)]
        solid = solid.faces('>Y').workplane().pushPoints(hole_positions).hole(m.hole_diameter)
        # optional gusset on outer corner of vertical leg
        if m.gusset:
            gusset = (
                cq.Workplane('XY')
                .polyline([
                    (0, 0),
                    (m.gusset_length, 0),
                    (m.gusset_length, m.gusset_thickness),
                    (0, m.gusset_thickness),
                ])
                .close()
                .extrude(m.bracket_thickness)
                .translate((m.leg_thickness, m.vertical_leg_height - m.gusset_thickness, 0))
            )
            solid = solid.union(gusset)
        self.model = solid

measures = Measures(
    horizontal_leg_length=70.0,
    vertical_leg_height=80.0,
    leg_thickness=10.0,
    bracket_thickness=8.0,
    inner_fillet_radius=3.0,
    hole_diameter=5.0,
    hole_count=4,
    hole_spacing=15.0,
    hole_edge_distance=10.0,
    gusset=True,
    gusset_length=20.0,
    gusset_thickness=5.0,
)

result = LBracket(cq.Workplane('XY'), measures).model