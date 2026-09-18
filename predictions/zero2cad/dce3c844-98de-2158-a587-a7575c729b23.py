import cadquery as cq
from types import SimpleNamespace as Measures

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        # Base L profile extrusion
        base = (
            cq.Workplane("XY")
            .polyline([
                (0, 0),
                (m.horizontal_length, 0),
                (m.horizontal_length, m.thickness),
                (m.thickness, m.thickness),
                (m.thickness, m.vertical_length),
                (0, m.vertical_length),
                (0, 0),
            ])
            .close()
            .extrude(m.thickness)
        )
        # Mounting holes on horizontal leg
        holes = (
            base.faces(">Z")
            .workplane()
            .pushPoints([
                (m.horizontal_length * 0.25, m.thickness / 2),
                (m.horizontal_length * 0.75, m.thickness / 2),
            ])
            .hole(m.mount_hole_diameter)
        )
        # Recessed pocket on vertical leg
        pocket = (
            holes.faces(">Z")
            .workplane()
            .center(m.thickness / 2, m.vertical_length / 2)
            .rect(m.pocket_width, m.pocket_height)
            .cutBlind(m.pocket_depth)
        )
        # Chamfer outer edges
        result = (
            pocket.edges("|Z")
            .chamfer(m.chamfer)
        )
        self.model = result

# Define parameters
measures = Measures(
    horizontal_length=80.0,
    vertical_length=60.0,
    thickness=10.0,
    mount_hole_diameter=6.0,
    pocket_width=20.0,
    pocket_height=30.0,
    pocket_depth=5.0,
    chamfer=1.0,
)

result = LBracket(cq.Workplane("XY"), measures).model