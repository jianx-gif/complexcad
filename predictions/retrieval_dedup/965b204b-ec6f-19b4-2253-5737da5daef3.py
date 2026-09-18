import cadquery as cq
from types import SimpleNamespace as Measures
import math

def csk_face_hole(self, diameter, csk_diameter, csk_angle, depth=None, offset=(0, 0)):
    if depth is None:
        depth = self.largestDimension()
    for face in self.objects:
        if isinstance(face, cq.Face):
            base_center = face.Center()
            # Apply planar offset in face local XY (assume face normal aligns with Z)
            offset_vec = cq.Vector(offset[0], offset[1], 0)
            center = base_center.add(offset_vec)
            normal = face.normalAt(base_center).multiply(-1)
            hole = cq.Solid.makeCylinder(0.5 * diameter, depth, center, normal)
            csk_radius = 0.5 * csk_diameter
            csk_height = csk_radius / math.tan(math.radians(0.5 * csk_angle))
            csk = cq.Solid.makeCone(csk_radius, 0.0, csk_height, center, normal)
            cut_obj = hole.fuse(csk)
            self = self.newObject([self.findSolid().cut(cut_obj)])
    return self

cq.Workplane.csk_face_hole = csk_face_hole

class MotionDetectorMount:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = measures
        self.build()
        self.model = self.base

    def build(self):
        m = self.measures
        base = (
            cq.Workplane('XY')
            .rect(m.back_width, m.back_height)
            .workplane(offset=m.base_thickness)
            .transformed(offset=(0, m.lip_offset_y, 0))
            .rect(m.lip_width, m.lip_height)
            .loft()
        )
        base = base.edges('>X or <X or >Y or <Y').chamfer(m.edge_chamfer)
        base = (
            base.faces('>Z')
            .workplane()
            .center(0, m.recess_center_y)
            .hole(m.recess_diameter, depth=m.recess_depth)
        )
        base = (
            base.faces('<Z')
            .csk_face_hole(
                diameter=m.set_screw_hole,
                csk_diameter=m.set_screw_head,
                csk_angle=m.set_screw_angle,
                depth=m.base_thickness + 2,
                offset=(-m.set_screw_spacing/2, 0)
            )
            .csk_face_hole(
                diameter=m.set_screw_hole,
                csk_diameter=m.set_screw_head,
                csk_angle=m.set_screw_angle,
                depth=m.base_thickness + 2,
                offset=(m.set_screw_spacing/2, 0)
            )
        )
        self.base = base

measures = Measures(
    back_width=80.0,
    back_height=40.0,
    base_thickness=8.0,
    lip_width=60.0,
    lip_height=12.0,
    lip_offset_y=10.0,
    edge_chamfer=0.8,
    recess_diameter=30.0,
    recess_depth=4.0,
    recess_center_y=5.0,
    set_screw_spacing=50.0,
    set_screw_hole=4.5,
    set_screw_head=8.0,
    set_screw_angle=90.0,
)

mount = MotionDetectorMount(cq.Workplane('XY'), measures)
result = mount.model