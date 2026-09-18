import cadquery as cq
from dataclasses import dataclass

@dataclass
class BracketMeasures:
    leg_length_x: float = 70.0
    leg_length_y: float = 50.0
    thickness: float = 8.0
    width: float = 20.0
    fillet_radius: float = 5.0
    hole_diameter: float = 0.6

class LMountBracket:
    def __init__(self, workplane, measures: BracketMeasures):
        self.wp = workplane
        self.m = measures
        self.model = None
        self.build()

    def build(self):
        m = self.m
        # Horizontal leg box
        horiz = (
            cq.Workplane("XY")
            .box(m.leg_length_x, m.thickness, m.width)
            .translate((m.leg_length_x / 2, m.thickness / 2, 0))
        )
        # Vertical leg box
        vert = (
            cq.Workplane("XY")
            .box(m.thickness, m.leg_length_y, m.width)
            .translate((m.thickness / 2, m.thickness + m.leg_length_y / 2, 0))
        )
        # Combine legs into L shape
        bracket = horiz.union(vert)
        # Add internal fillet at the joint (inner corner)
        bracket = bracket.edges("|Z and <X and >Y").fillet(m.fillet_radius)
        # Add through hole on vertical leg
        bracket = (
            bracket
            .faces(">Z")
            .workplane()
            .center(m.thickness / 2, m.thickness + m.leg_length_y / 2)
            .hole(m.hole_diameter)
        )
        self.model = bracket

# Create the part
measures = BracketMeasures()
result = LMountBracket(cq.Workplane("XY"), measures).model
