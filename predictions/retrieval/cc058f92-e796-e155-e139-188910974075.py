import cadquery as cq
from types import SimpleNamespace as Measures

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        # Base L shape extruded to thickness
        base = (
            cq.Workplane('XY')
            .polyline([
                (0, 0),
                (0, m.vertical_height),
                (m.leg_thickness, m.vertical_height),
                (m.leg_thickness, m.leg_thickness),
                (m.horizontal_length, m.leg_thickness),
                (m.horizontal_length, 0),
                (0, 0)
            ])
            .close()
            .extrude(m.thickness)
        )
        # Chamfer inner corner by cutting a 45-degree wedge
        wedge = (
            cq.Workplane('XY')
            .polygon(3, 2 * m.chamfer_size)
            .translate((m.chamfer_size, m.chamfer_size, 0))
            .rotate((0, 0, 0), (0, 0, 1), 45)
            .extrude(m.thickness)
        )
        bracket = base.cut(wedge)
        # Through through-hole on vertical arm (centered)
        hole_cylinder = (
            cq.Workplane('XY')
            .center(m.leg_thickness / 2, m.vertical_height * 0.5)
            .circle(m.hole_clearance / 2)
            .extrude(m.thickness + 2)
        )
        bracket = bracket.cut(hole_cylinder)
        # Mounting holes pattern on horizontal arm (front face)
        bracket = (
            bracket.faces('>X')
            .workplane()
            .center(m.horizontal_length - m.mount_edge_offset, m.leg_thickness / 2)
            .rect(m.mount_hole_spacing, m.mount_hole_spacing, forConstruction=True)
            .vertices()
            .hole(m.mount_hole_clearance)
        )
        # Optional gussets on outer corners
        if m.gusset_enabled:
            # Horizontal gusset
            gusset_h = (
                cq.Workplane('XY')
                .moveTo(m.horizontal_length, 0)
                .lineTo(m.horizontal_length + m.gusset_length, 0)
                .lineTo(m.horizontal_length + m.gusset_length, m.gusset_thickness)
                .lineTo(m.horizontal_length, m.gusset_thickness)
                .close()
                .extrude(m.thickness)
            )
            # Vertical gusset
            gusset_v = (
                cq.Workplane('XY')
                .moveTo(0, m.vertical_height)
                .lineTo(0, m.vertical_height + m.gusset_length)
                .lineTo(m.gusset_thickness, m.vertical_height + m.gusset_length)
                .lineTo(m.gusset_thickness, m.vertical_height)
                .close()
                .extrude(m.thickness)
            )
            bracket = bracket.union(gusset_h).union(gusset_v)
        self.model = bracket

# Parameter definitions within max 100 units
measures = Measures(
    horizontal_length=80.0,
    vertical_height=70.0,
    leg_thickness=8.0,
    thickness=10.0,
    chamfer_size=4.0,
    hole_clearance=5.0,
    mount_hole_spacing=30.0,
    mount_hole_clearance=5.0,
    mount_edge_offset=10.0,
    gusset_enabled=True,
    gusset_length=15.0,
    gusset_thickness=5.0,
)

result = LBracket(cq.Workplane('XY'), measures).model