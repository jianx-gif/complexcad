import cadquery as cq
from types import SimpleNamespace as Measures

class LBracket:
    def __init__(self, workplane, measures):
        self.wp = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        base = (
            cq.Workplane("XZ")
            .moveTo(0, 0)
            .lineTo(m.arm_thickness, 0)
            .lineTo(m.arm_thickness, m.vertical_arm_length)
            .lineTo(m.horizontal_arm_length, m.vertical_arm_length)
            .radiusArc((m.horizontal_arm_length + m.outer_corner_radius, m.vertical_arm_length + m.outer_corner_radius), m.outer_corner_radius)
            .lineTo(m.horizontal_arm_length + m.outer_corner_radius, m.outer_corner_radius)
            .lineTo(0, m.outer_corner_radius)
            .close()
        )
        model = base.revolve(360, (0, 0, 0), (0, 1, 0))
        vertical_hole_center = m.arm_thickness / 2.0
        vertical_hole = (
            cq.Workplane("XZ")
            .transformed(offset=cq.Vector(vertical_hole_center, 0, 0))
            .circle(m.vertical_hole_diameter / 2.0)
            .extrude(m.vertical_arm_length + 2 * m.outer_corner_radius)
        )
        model = model.cut(vertical_hole)
        slot_center = m.horizontal_arm_length / 2.0 + m.arm_thickness / 2.0
        slot = (
            cq.Workplane("XZ")
            .transformed(offset=cq.Vector(slot_center, 0, 0))
            .rect(m.slot_length, m.slot_width)
            .extrude(m.arm_thickness * 2)
        )
        model = model.cut(slot)
        rib_center_radius = m.arm_thickness / 2.0
        rib = (
            cq.Workplane("XZ")
            .transformed(offset=cq.Vector(rib_center_radius, 0, 0))
            .center(0, m.vertical_arm_length / 2.0)
            .rect(m.rib_width, m.rib_height)
            .extrude(m.rib_depth)
        )
        model = model.union(rib)
        self.model = model

measures = Measures(
    vertical_arm_length=60.0,
    horizontal_arm_length=80.0,
    arm_thickness=8.0,
    outer_corner_radius=5.0,
    vertical_hole_diameter=5.0,
    slot_width=7.0,
    slot_length=20.0,
    rib_width=6.0,
    rib_height=10.0,
    rib_depth=8.0,
)

result = LBracket(cq.Workplane("XY"), measures).model