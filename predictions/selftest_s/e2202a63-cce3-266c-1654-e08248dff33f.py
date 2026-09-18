import cadquery as cq
from types import SimpleNamespace as Measures

socket_height = 70.0
outer_radius = 30.0
inner_radius = 20.0
lip_thickness = 2.0
pocket_start = 30.0
pocket_height = 10.0
lip_height = 5.0
pilot_diameter = 5.0
chamfer_len = 2.0
boss_height = 8.0
# boss radius set to intersect outer wall
boss_radius = inner_radius + 0.5 * lip_thickness

class XMountSocket:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = measures
        self.build()
        self.model = self.result

    def build(self):
        m = self.measures
        profile_wp = (
            cq.Workplane("XZ")
            .polyline([
                (m.outer_radius, 0),
                (m.outer_radius, m.pocket_start),
                (m.inner_radius + m.lip_thickness, m.pocket_start),
                (m.inner_radius + m.lip_thickness, m.pocket_start + m.pocket_height),
                (m.inner_radius, m.pocket_start + m.pocket_height),
                (m.inner_radius, m.socket_height - m.lip_height),
                (m.outer_radius, m.socket_height - m.lip_height),
                (m.outer_radius, m.socket_height),
                (0, m.socket_height),
                (0, 0)
            ])
            .close()
        )
        solid = profile_wp.revolve()
        wp = cq.Workplane("XY").add(solid)
        pocket = (
            cq.Workplane("XY")
            .center(0, 0)
            .circle(m.inner_radius - m.lip_thickness)
            .extrude(m.pocket_start + m.pocket_height)
        )
        wp = wp.cut(pocket)
        wp = wp.faces("<Z").workplane().hole(m.pilot_diameter)
        wp = wp.faces(">Z").edges().chamfer(m.chamfer_len)
        boss = (
            cq.Workplane("XY")
            .center(0, 0)
            .circle(m.boss_radius)
            .extrude(m.boss_height)
        )
        wp = wp.union(boss)
        self.result = wp

measures = Measures(
    socket_height=socket_height,
    outer_radius=outer_radius,
    inner_radius=inner_radius,
    lip_thickness=lip_thickness,
    pocket_start=pocket_start,
    pocket_height=pocket_height,
    lip_height=lip_height,
    pilot_diameter=pilot_diameter,
    chamfer_len=chamfer_len,
    boss_height=boss_height,
    boss_radius=boss_radius,
)

result = XMountSocket(cq.Workplane("XY"), measures).model
