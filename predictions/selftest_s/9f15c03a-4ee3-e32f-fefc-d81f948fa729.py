import cadquery as cq
import copy
from types import SimpleNamespace as Measures

class XMountSocket:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = copy.deepcopy(measures)
        self.build()

    def build(self):
        m = self.measures
        # Create outer profile with front tab using a single polyline
        outer_profile = (
            cq.Workplane('XY')
            .center(-0.5 * m.width, -0.5 * m.depth)
            .polyline([
                (0, 0),
                (m.width * 0.25, 0),
                (m.width * 0.25, -m.tab_height),
                (m.width * 0.75, -m.tab_height),
                (m.width * 0.75, 0),
                (m.width, 0),
                (m.width, m.depth),
                (0, m.depth),
                (0, 0)
            ])
            .close()
        )
        # Extrude to give thickness
        solid = outer_profile.extrude(m.height)
        # Hollow out by shelling inward
        hollow = solid.shell(-m.wall_thickness)
        # Fillet outer corners (top edges)
        filleted = hollow.edges('>Z and (|X or |Y)').fillet(m.corner_radius)
        # Chamfer bottom edges for safety
        chamfered = filleted.edges('<Z and (|X or |Y)').chamfer(m.chamfer)
        # Central mounting hole through top face
        result = chamfered.faces('>Z').hole(m.hole_diameter)
        self.model = result

# Define measures within scale constraint (max dimension 100)
measures = Measures(
    width = 80.0,
    depth = 60.0,
    height = 20.0,
    wall_thickness = 4.0,
    corner_radius = 5.0,
    chamfer = 1.0,
    tab_height = 8.0,
    hole_diameter = 20.0,
)

socket = XMountSocket(cq.Workplane('XY'), measures)
result = socket.model