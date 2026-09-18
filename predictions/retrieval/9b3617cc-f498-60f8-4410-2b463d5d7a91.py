import cadquery as cq
import copy
from types import SimpleNamespace as Measures

a_outer_radius = 20.0
a_inner_radius = 12.0
a_socket_length = 30.0
a_base_height = 5.0
a_boss_radius = 8.0
a_boss_height = 6.0
a_chamfer = 0.8
hole_diameter = 4.0
hole_pattern_radius = 15.0

class XMountSocket:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = copy.deepcopy(measures)
        self.build()
    def build(self):
        m = self.measures
        profile = (
            cq.Workplane("XZ")
            .moveTo(0, 0)
            .lineTo(m.outer_radius, 0)
            .lineTo(m.outer_radius, m.base_height)
            .lineTo(m.inner_radius, m.base_height)
            .lineTo(m.inner_radius, m.socket_length)
            .lineTo(0, m.socket_length)
            .close()
        )
        socket = profile.revolve()
        boss = (
            cq.Workplane("XY")
            .circle(m.boss_radius)
            .extrude(m.boss_height)
        )
        base = socket.union(boss)
        base = base.edges(">Z").chamfer(m.chamfer)
        hole_positions = [
            (m.hole_pattern_radius, 0),
            (0, m.hole_pattern_radius),
            (-m.hole_pattern_radius, 0),
            (0, -m.hole_pattern_radius)
        ]
        holes = (
            cq.Workplane("XY")
            .pushPoints(hole_positions)
            .circle(m.hole_diameter / 2)
            .extrude(m.socket_length)
        )
        result_solid = base.cut(holes)
        self.model = result_solid

measures = Measures(
    outer_radius = a_outer_radius,
    inner_radius = a_inner_radius,
    socket_length = a_socket_length,
    base_height = a_base_height,
    boss_radius = a_boss_radius,
    boss_height = a_boss_height,
    chamfer = a_chamfer,
    hole_diameter = hole_diameter,
    hole_pattern_radius = hole_pattern_radius,
)

result = XMountSocket(cq.Workplane("XY"), measures).model