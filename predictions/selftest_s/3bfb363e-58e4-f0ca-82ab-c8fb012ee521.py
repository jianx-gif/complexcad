import cadquery as cq
from types import SimpleNamespace as Measures

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        base = (
            cq.Workplane('XY')
            .polyline([
                (0, 0),
                (m.leg_length_x, 0),
                (m.leg_length_x, m.thickness),
                (m.thickness, m.thickness),
                (m.thickness, m.leg_length_y),
                (0, m.leg_length_y),
                (0, 0)
            ])
            .close()
            .extrude(m.thickness_z)
        )
        boss_center_x = m.thickness / 2
        boss_center_y = m.thickness / 2
        with_boss = (
            base.faces('>Z')
            .workplane(centerOption='CenterOfBoundBox')
            .center(boss_center_x - m.leg_length_x/2, boss_center_y - m.leg_length_y/2)
            .rect(m.boss_width, m.boss_depth)
            .extrude(m.boss_height)
        )
        with_hole = (
            with_boss.faces('>Z')
            .workplane(centerOption='CenterOfBoundBox')
            .center(boss_center_x - m.leg_length_x/2, boss_center_y - m.leg_length_y/2)
            .hole(m.hole_diameter)
        )
        horiz_y = -m.leg_length_y/2 + m.thickness/2
        horiz_points = [
            (-m.leg_length_x/2 + m.mount_margin, horiz_y),
            (m.leg_length_x/2 - m.mount_margin, horiz_y)
        ]
        with_horiz_holes = (
            with_hole.faces('>Z')
            .workplane(centerOption='CenterOfBoundBox')
            .pushPoints(horiz_points)
            .hole(m.mount_hole_dia)
        )
        vert_x = -m.leg_length_x/2 + m.thickness/2
        vert_points = [
            (vert_x, -m.leg_length_y/2 + m.mount_margin),
            (vert_x, m.leg_length_y/2 - m.mount_margin)
        ]
        with_all_holes = (
            with_horiz_holes.faces('>Z')
            .workplane(centerOption='CenterOfBoundBox')
            .pushPoints(vert_points)
            .hole(m.mount_hole_dia)
        )
        # Fillet inner concave corner before chamfer
        inner_fillet = (
            with_all_holes.edges('(<X and <Y) and |Z')
            .fillet(m.fillet_radius)
        )
        # Chamfer outer edges (right and top edges only to avoid inner fillet conflict)
        final = (
            inner_fillet.edges('>X or >Y')
            .chamfer(m.chamfer_dist)
        )
        self.model = final

measures = Measures(
    leg_length_x=80.0,
    leg_length_y=60.0,
    thickness=15.0,
    thickness_z=15.0,
    boss_width=12.0,
    boss_depth=12.0,
    boss_height=20.0,
    hole_diameter=10.0,
    fillet_radius=5.0,
    chamfer_dist=1.0,
    mount_margin=20.0,
    mount_hole_dia=5.0,
)

result = LBracket(cq.Workplane('XY'), measures).model
