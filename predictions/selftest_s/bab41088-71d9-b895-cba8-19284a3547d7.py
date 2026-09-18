import cadquery as cq

# Parameters (max dimension 100 units)
length = 80.0
trap_top_width = 30.0
trap_bottom_width = 50.0
trap_height = 40.0
circle_radius = 20.0
rib_width = 10.0
rib_height = 6.0
rib_offset = 5.0
chamfer_dist = 1.0
notch_width = 12.0
notch_depth = 5.0
notch_position = 0.4

half_top = trap_top_width / 2.0
half_bottom = trap_bottom_width / 2.0

class LoftedPart:
    def __init__(self):
        self.model = None

    def _trapezoid_points(self):
        return [
            (-half_bottom, 0),
            (half_bottom, 0),
            (half_top, trap_height),
            (-half_top, trap_height),
            (-half_bottom, 0)
        ]

    def _create_loft(self):
        pts = self._trapezoid_points()
        loft = (
            cq.Workplane('XY')
            .polyline(pts).close()
            .workplane(offset=length)
            .circle(circle_radius)
            .loft(combine=True)
        )
        return loft

    def _add_notch(self, solid):
        notch_center_z = length * notch_position
        notch = (
            cq.Workplane('YZ')
            .center(0, notch_center_z)
            .rect(notch_width, notch_depth)
            .extrude(half_bottom * 2 + 2)
            .translate((- (half_bottom + 1), 0, 0))
        )
        return solid.cut(notch)

    def _rib(self):
        x_center = half_bottom - rib_offset - rib_width / 2.0
        rib = (
            cq.Workplane('XY')
            .center(x_center, 0)
            .rect(rib_width, rib_height)
            .extrude(length)
        )
        rib_chamfered = rib.edges().chamfer(chamfer_dist)
        return rib_chamfered

    def build(self):
        loft_body = self._create_loft()
        loft_notched = self._add_notch(loft_body)
        rib_body = self._rib()
        combined = loft_notched.union(rib_body)
        self.model = combined
        return combined

part = LoftedPart()
result = part.build()
