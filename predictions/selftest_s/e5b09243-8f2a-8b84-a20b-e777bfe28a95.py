import cadquery as cq
from types import SimpleNamespace as Measures

def csk_face_hole(self, diameter, csk_diameter, csk_angle, depth=None, offset=None):
    context_solid = self.findSolid()
    if depth is None:
        depth = self.largestDimension()
    if offset is None:
        offset = (0.0, 0.0)
    for face in self.objects:
        if isinstance(face, cq.Face):
            origin = face.Center()
            normal = face.normalAt()
            if normal.normalized() == cq.Vector(0, 0, 1):
                x_dir = cq.Vector(1, 0, 0)
            elif normal.normalized() == cq.Vector(0, 0, -1):
                x_dir = cq.Vector(-1, 0, 0)
            else:
                x_dir = cq.Vector(0, 0, 1).cross(normal)
            plane = cq.Plane(origin, x_dir, normal)
            plane.setOrigin2d(*offset)
            bore_dir = normal.multiply(-1)
            center = plane.toWorldCoords((0, 0, 0))
            hole = cq.Solid.makeCylinder(0.5 * diameter, depth, center, bore_dir)
            csk_radius = 0.5 * csk_diameter
            csk_height = csk_radius / cq.tan(cq.radians(0.5 * csk_angle))
            csk = cq.Solid.makeCone(csk_radius, 0.0, csk_height, center, bore_dir)
            csk_hole = hole.fuse(csk)
            context_solid = context_solid.cut(csk_hole)
    return self.newObject([context_solid])

cq.Workplane.csk_face_hole = csk_face_hole

class HydraulicPumpBracket:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = measures
        self.build()
    def build(self):
        m = self.measures
        base = (
            cq.Workplane("XZ")
            .rect(m.base_width, m.base_height)
            .workplane(offset=m.thickness)
            .transformed(rotate=(0, m.bend_angle, 0))
            .rect(m.tab_width, m.tab_height)
            .loft()
            .chamfer(m.edge_chamfer)
        )
        pocket = (
            base
            .faces(">Y")
            .workplane(centerOption='CenterOfMass')
            .rect(m.pocket_width, m.pocket_length)
            .cutBlind(-m.pocket_depth)
        )
        holes = (
            pocket
            .faces("<Y")
            .workplane()
            .rarray(m.screw_spacing, 0, 3, 1)
            .csk_face_hole(
                diameter=m.screw_hole_dia,
                csk_diameter=m.screw_head_dia,
                csk_angle=m.screw_head_angle,
                offset=(0, 0)
            )
        )
        self.model = holes

# Define measures
measures = Measures(
    base_width=80.0,
    base_height=60.0,
    thickness=8.0,
    bend_angle=45.0,
    tab_width=40.0,
    tab_height=30.0,
    edge_chamfer=1.0,
    pocket_width=20.0,
    pocket_length=30.0,
    pocket_depth=6.0,
    screw_hole_dia=4.0,
    screw_head_dia=7.0,
    screw_head_angle=90.0,
    screw_spacing=25.0,
)

result = HydraulicPumpBracket(cq.Workplane("XY"), measures).model