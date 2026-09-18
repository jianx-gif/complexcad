import cadquery as cq
from types import SimpleNamespace as Measures

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        # Base L profile sketch
        base = (
            cq.Workplane("XY")
            .polyline([
                (0, 0),
                (m.leg_thickness, 0),
                (m.leg_thickness, m.vertical_leg_length),
                (m.leg_thickness + m.horizontal_leg_length, m.vertical_leg_length),
                (m.leg_thickness + m.horizontal_leg_length, m.vertical_leg_length + m.leg_thickness),
                (0, m.vertical_leg_length + m.leg_thickness),
                (0, 0),
            ])
            .close()
            .extrude(m.leg_thickness)
        )
        # Recessed pocket on horizontal leg
        pocket = (
            base.faces(">Z")
            .workplane()
            .center(m.leg_thickness + m.horizontal_leg_length/2, m.vertical_leg_length + m.leg_thickness/2)
            .rect(m.pocket_width, m.pocket_length)
            .cutBlind(m.pocket_depth)
        )
        # Fillet inner corner
        filleted = pocket.edges().fillet(m.fillet_radius)
        # Mounting holes on vertical leg
        holes = (
            filleted.faces(">Z")
            .workplane()
            .center(m.leg_thickness/2, m.vertical_leg_length/2)
            .rarray(m.hole_spacing, 0, 2, 1)
            .hole(m.hole_diameter)
        )
        self.model = holes

# Define parameters
measures = Measures(
    leg_thickness=10.0,
    vertical_leg_length=60.0,
    horizontal_leg_length=70.0,
    pocket_width=30.0,
    pocket_length=20.0,
    pocket_depth=5.0,
    fillet_radius=1.2,
    hole_diameter=5.0,
    hole_spacing=30.0,
)

result = LBracket(cq.Workplane("XY"), measures).model