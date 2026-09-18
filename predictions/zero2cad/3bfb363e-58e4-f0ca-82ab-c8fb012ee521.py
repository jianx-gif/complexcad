import cadquery as cq
from types import SimpleNamespace as Measures

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        # Base L shape
        base = (
            cq.Workplane("XY")
            .polyline([
                (0, 0),
                (m.leg_length_x, 0),
                (m.leg_length_x, m.thickness),
                (m.thickness, m.thickness),
                (m.thickness, m.leg_length_y),
                (0, m.leg_length_y),
                (0, 0),
            ])
            .close()
            .extrude(m.thickness)
        )
        # Fillet inner corner
        base = base.edges("|Z and <X and <Y").fillet(m.fillet_radius)
        # Chamfer outer edges
        base = base.edges(">X or >Y").chamfer(m.chamfer_distance)
        # Reinforcement rib at inner corner
        rib = (
            cq.Workplane("XY")
            .rect(m.rib_width, m.rib_height)
            .extrude(m.rib_length)
            .translate((m.thickness/2, m.thickness/2, m.thickness))
        )
        # Combine base and rib
        combined = base.union(rib)
        # Blind hole on horizontal leg
        combined = (
            combined.faces(">Z")
            .workplane()
            .center(m.leg_length_x/2, m.thickness/2)
            .hole(m.hole_diameter, depth=m.hole_depth)
        )
        self.model = combined

# Define parameters
measures = Measures(
    leg_length_x=80.0,
    leg_length_y=60.0,
    thickness=15.0,
    fillet_radius=5.0,
    chamfer_distance=1.0,
    rib_width=12.0,
    rib_height=12.0,
    rib_length=20.0,
    hole_diameter=8.0,
    hole_depth=10.0,
)

result = LBracket(cq.Workplane("XY"), measures).model