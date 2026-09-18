import cadquery as cq
from types import SimpleNamespace as Measures
class BearingSpacerRing:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = measures
        self.build()
    def build(self):
        m = self.measures
        outer = m.outer_radius
        inner = m.inner_radius
        thickness = m.spacer_thickness
        rib_thick = m.rib_thickness
        rib_h = m.rib_height
        chamfer = m.chamfer_distance
        profile = (
            cq.Workplane('XZ')
            .moveTo(0, 0)
            .lineTo(outer, 0)
            .lineTo(outer, thickness)
            .lineTo(inner + rib_thick, thickness)
            .lineTo(inner + rib_thick, thickness - rib_h)
            .lineTo(inner, thickness - rib_h)
            .lineTo(inner, 0)
            .close()
        )
        solid = profile.revolve()
        hole = cq.Workplane('XY').circle(inner).extrude(thickness + 2)
        solid = solid.cut(hole)
        solid = solid.edges('>Z').chamfer(chamfer)
        self.model = solid

measures = Measures(
    outer_radius=30.0,
    inner_radius=12.0,
    spacer_thickness=10.0,
    rib_thickness=4.0,
    rib_height=6.0,
    chamfer_distance=1.0
)
result = BearingSpacerRing(cq.Workplane('XY'), measures).model
