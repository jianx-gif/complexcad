import cadquery as cq
from types import SimpleNamespace as Measures

bracket_height = 60.0
bracket_thickness = 5.0
outer_radius = 30.0
inner_radius = outer_radius - bracket_thickness
tab_height = 20.0
tab_extra = 8.0
hole_diameter = 5.0
hole_spacing = 15.0
revolve_angle = 60.0

class AlarmBracket:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        pts = [
            (m.inner_radius, -m.bracket_height/2),                     # bottom inner
            (m.outer_radius, -m.bracket_height/2),                     # bottom outer
            (m.outer_radius, -m.tab_height/2),                        # up to tab start
            (m.outer_radius + m.tab_extra, -m.tab_height/2),           # outward tab bottom
            (m.outer_radius + m.tab_extra, m.tab_height/2),            # upward tab top
            (m.outer_radius, m.tab_height/2),                         # back to outer radius
            (m.outer_radius, m.bracket_height/2),                     # top outer
            (m.inner_radius, m.bracket_height/2),                     # top inner
        ]
        profile = cq.Workplane("XY").polyline(pts).close()
        part = profile.revolve(m.revolve_angle)
        hole_positions = [(0, -m.hole_spacing), (0, 0), (0, m.hole_spacing)]
        part = (
            part.faces(">X")
            .workplane()
            .pushPoints(hole_positions)
            .hole(m.hole_diameter)
        )
        self.model = part

measures = Measures(
    bracket_height=bracket_height,
    bracket_thickness=bracket_thickness,
    outer_radius=outer_radius,
    inner_radius=inner_radius,
    tab_height=tab_height,
    tab_extra=tab_extra,
    hole_diameter=hole_diameter,
    hole_spacing=hole_spacing,
    revolve_angle=revolve_angle,
)

bracket = AlarmBracket(cq.Workplane("XY"), measures)
result = bracket.model
