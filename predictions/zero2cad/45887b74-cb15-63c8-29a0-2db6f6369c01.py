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
            .moveTo(0, 0)
            .lineTo(m.horizontal_leg_length, 0)
            .lineTo(m.horizontal_leg_length, m.leg_thickness)
            .lineTo(m.leg_thickness, m.leg_thickness)
            .lineTo(m.leg_thickness, m.vertical_leg_length)
            .close()
            .extrude(m.bracket_depth)
        )
        # Fillet inner corner (vertical edge at inner corner)
        inner_edge = base.edges().filter(
            lambda e: abs(e.Center().x - m.leg_thickness) < 1e-3 and abs(e.Center().y - m.leg_thickness) < 1e-3
        )
        base = inner_edge.fillet(m.fillet_radius)
        # Add mounting holes on vertical leg (face >X)
        base = (
            base.faces(">X")
            .workplane(centerOption="CenterOfBoundBox")
            .moveTo(m.leg_thickness/2, m.vertical_leg_length/2)
            .rarray(m.hole_spacing, 0, 2, 1)
            .hole(m.hole_diameter)
        )
        # Add mounting holes on horizontal leg (face >Y)
        base = (
            base.faces(">Y")
            .workplane(centerOption="CenterOfBoundBox")
            .moveTo(m.horizontal_leg_length/2, m.leg_thickness/2)
            .rarray(m.hole_spacing, 0, 2, 1)
            .hole(m.hole_diameter)
        )
        # Add a rectangular pocket on horizontal leg for weight reduction
        base = (
            base.faces(">Y")
            .workplane(centerOption="CenterOfBoundBox")
            .moveTo(m.horizontal_leg_length/2, m.leg_thickness/2)
            .rect(m.pocket_width, m.pocket_height)
            .cutBlind(-m.pocket_depth)
        )
        self.model = base

# Define parameters respecting max dimension 100 units
measures = Measures(
    horizontal_leg_length=70.0,
    vertical_leg_length=50.0,
    leg_thickness=10.0,
    bracket_depth=12.0,
    fillet_radius=2.0,
    hole_diameter=4.0,
    hole_spacing=20.0,
    pocket_width=30.0,
    pocket_height=6.0,
    pocket_depth=4.0,
)

result = LBracket(cq.Workplane("XY"), measures).model