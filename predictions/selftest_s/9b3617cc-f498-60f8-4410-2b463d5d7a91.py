import cadquery as cq
from types import SimpleNamespace as Measures

class WallShelfSupport:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        # Profile for turned shaft (excluding base disc)
        profile = (
            cq.Workplane("XZ")
            .moveTo(0, 0)
            .lineTo(m.base.radius, 0)
            .lineTo(m.transition.radius, m.transition.height)
            .lineTo(m.shaft.radius, m.transition.height + m.shaft.height)
            .lineTo(0, m.transition.height + m.shaft.height)
            .close()
        )
        turned_body = profile.revolve()
        # Raise turned body above base disc thickness
        turned_body = turned_body.translate((0, 0, m.base.thickness))
        # Base disc
        base_disc = cq.Workplane("XY").circle(m.base.radius).extrude(m.base.thickness)
        # Combine
        solid = base_disc.union(turned_body)
        solid = solid.edges().chamfer(m.base.chamfer)
        # Central threaded clearance hole
        solid = (
            solid
            .faces(">Z")
            .workplane()
            .hole(m.central_hole.diameter, depth=m.central_hole.depth)
        )
        # Mounting holes on base disc bottom
        mount_radius = m.mount.hole_spacing / 2.0
        hole_positions = [
            ( mount_radius, 0),
            (-mount_radius, 0),
            (0,  mount_radius),
            (0, -mount_radius)
        ]
        solid = (
            solid
            .faces("<Z")
            .workplane()
            .pushPoints(hole_positions)
            .hole(m.mount.hole_diameter, depth=m.mount.hole_depth)
        )
        self.model = solid

measures = Measures(
    base=Measures(
        radius=30.0,
        thickness=10.0,
        chamfer=1.0
    ),
    transition=Measures(
        radius=20.0,
        height=5.0
    ),
    shaft=Measures(
        radius=12.0,
        height=40.0
    ),
    mount=Measures(
        hole_diameter=5.0,
        hole_spacing=45.0,
        hole_depth=8.0
    ),
    central_hole=Measures(
        diameter=6.0,
        depth=20.0
    )
)

support = WallShelfSupport(cq.Workplane("XZ"), measures)
result = support.model