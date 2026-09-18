import cadquery as cq
from types import SimpleNamespace as Measures
import copy

class XMountSocket:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = copy.deepcopy(measures)
        self.build()

    def build(self):
        m = self.measures
        # Base block
        block = (
            cq.Workplane("XY")
            .box(m.block_width, m.block_depth, m.block_height, centered=(True, True, False))
        )
        # Central cylinder
        cylinder = (
            cq.Workplane("XY")
            .circle(m.cylinder_radius)
            .extrude(m.cylinder_height)
        )
        # Union of block and cylinder
        body = block.union(cylinder)
        # Pocket cut on top surface
        pocket = (
            cq.Workplane("XY")
            .workplane(offset=m.block_height)  # start at top of block
            .rect(m.pocket_width, m.pocket_depth)
            .extrude(-m.pocket_depth)  # cut downwards
        )
        body = body.cut(pocket)
        # Counterbore hole at pocket center
        body = (
            body.faces(">Z")
            .workplane()
            .hole(m.counterbore_diameter, depth=m.counterbore_depth)
        )
        # Fillet interior pocket edges
        body = (
            body.edges("|Z and >Y and <X")
            .fillet(m.fillet_radius)
        )
        # Chamfer outer edges of the whole part for safety
        body = body.edges(">Z or <Z").chamfer(m.chamfer_distance)
        self.model = body

# Define measures with a max dimension of 100 units
measures = Measures(
    block_width=80.0,
    block_depth=60.0,
    block_height=30.0,
    cylinder_radius=20.0,
    cylinder_height=30.0,
    pocket_width=40.0,
    pocket_depth=20.0,
    counterbore_diameter=12.0,
    counterbore_depth=15.0,
    fillet_radius=2.0,
    chamfer_distance=1.0,
)

result = XMountSocket(cq.Workplane("XY"), measures).model