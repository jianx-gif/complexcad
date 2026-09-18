import cadquery as cq
from types import SimpleNamespace as Measures

# Define parameters
short_leg_length = 50.0
long_leg_length = 80.0
leg_thickness = 6.0
bracket_depth = 8.0
counterbore_clearance = 4.0
counterbore_diameter = 6.5
counterbore_depth = 4.0
blind_hole_diameter = 4.0
blind_hole_depth = 5.0
blind_hole_start = 10.0
blind_hole_spacing = 15.0
chamfer_size = 1.0

measures = Measures(
    short_leg_length=short_leg_length,
    long_leg_length=long_leg_length,
    leg_thickness=leg_thickness,
    bracket_depth=bracket_depth,
    counterbore_clearance=counterbore_clearance,
    counterbore_diameter=counterbore_diameter,
    counterbore_depth=counterbore_depth,
    blind_hole_diameter=blind_hole_diameter,
    blind_hole_depth=blind_hole_depth,
    blind_hole_start=blind_hole_start,
    blind_hole_spacing=blind_hole_spacing,
    chamfer_size=chamfer_size,
)

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        # Sketch L profile
        pts = [
            (0, 0),
            (m.short_leg_length, 0),
            (m.short_leg_length, m.leg_thickness),
            (m.leg_thickness, m.leg_thickness),
            (m.leg_thickness, m.leg_thickness + m.long_leg_length),
            (0, m.leg_thickness + m.long_leg_length),
        ]
        self.model = (
            cq.Workplane("XY")
            .polyline(pts)
            .close()
            .extrude(m.bracket_depth)
        )
        # Mass‑centered counterbore at junction (inner corner)
        self.model = (
            self.model.faces(">Z")
            .workplane()
            .center(0, 0)
            .cboreHole(m.counterbore_clearance, m.counterbore_diameter, m.counterbore_depth)
        )
        # Four blind holes on long leg
        hole_points = []
        for i in range(4):
            x = m.leg_thickness / 2
            y = m.leg_thickness + m.blind_hole_start + i * m.blind_hole_spacing
            hole_points.append((x, y))
        self.model = (
            self.model.faces(">Z")
            .workplane()
            .pushPoints(hole_points)
            .hole(m.blind_hole_diameter, depth=m.blind_hole_depth)
        )
        # Chamfer outer edges for safety
        self.model = self.model.edges("|Z").chamfer(m.chamfer_size)

result = LBracket(cq.Workplane("XY"), measures).model
