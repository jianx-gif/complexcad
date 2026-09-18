import cadquery as cq
from types import SimpleNamespace as Measures

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        # Base L profile
        base = (
            cq.Workplane("XY")
            .polyline([
                (0, 0),
                (m.leg_width, 0),
                (m.leg_width, m.vertical_leg_length),
                (m.leg_width + m.horizontal_leg_length, m.vertical_leg_length),
                (m.leg_width + m.horizontal_leg_length, m.vertical_leg_length + m.leg_width),
                (0, m.vertical_leg_length + m.leg_width),
                (0, 0),
            ])
            .close()
            .extrude(m.thickness)
        )
        # Recessed pocket on horizontal leg
        pocket = (
            base.faces(">Z")
            .workplane()
            .center(m.leg_width + m.horizontal_leg_length / 2, m.vertical_leg_length + m.leg_width / 2)
            .rect(m.pocket_width, m.pocket_length)
            .cutBlind(-m.pocket_depth)
        )
        # Through hole on vertical leg
        hole = (
            pocket.faces(">Z")
            .workplane()
            .center(m.leg_width / 2, m.vertical_leg_length / 2)
            .hole(m.hole_diameter)
        )
        # Mounting holes on vertical leg (two holes)
        mount = (
            hole.faces(">Z")
            .workplane()
            .center(m.leg_width / 2, m.vertical_leg_length / 2)
            .rarray(m.mount_spacing, 0, 2, 1)
            .hole(m.mount_hole_diameter)
        )
        # Gusset reinforcement at inner corner
        gusset = (
            cq.Workplane("XY")
            .polyline([
                (0, 0),
                (m.gusset_width, 0),
                (0, m.gusset_height),
                (0, 0),
            ])
            .close()
            .extrude(m.thickness)
        )
        self.model = mount.union(gusset)

# Define parameters
measures = Measures(
    leg_width=30.0,
    vertical_leg_length=60.0,
    horizontal_leg_length=70.0,
    thickness=8.0,
    pocket_width=20.0,
    pocket_length=40.0,
    pocket_depth=5.0,
    hole_diameter=10.0,
    mount_hole_diameter=5.0,
    mount_spacing=40.0,
    gusset_width=15.0,
    gusset_height=15.0,
)

result = LBracket(cq.Workplane("XY"), measures).model