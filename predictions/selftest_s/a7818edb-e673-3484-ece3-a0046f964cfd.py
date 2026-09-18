import cadquery as cq
from types import SimpleNamespace as Measures
import math

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
            csk_height = csk_radius / math.tan(math.radians(0.5 * csk_angle))
            csk = cq.Solid.makeCone(csk_radius, 0.0, csk_height, center, bore_dir)
            csk_hole = hole.fuse(csk)
            context_solid = context_solid.cut(csk_hole)
    return self.newObject([context_solid])

cq.Workplane.csk_face_hole = csk_face_hole

measures = Measures(
    outer_width=70.0,
    outer_height=80.0,
    thickness=12.0,
    flange_thickness=8.0,
    web_thickness=6.0,
    chamfer=0.8,
    mount_hole_dia=4.5,
    mount_hole_spacing=30.0,
    set_screw_hole_dia=3.0,
    set_screw_head_dia=6.0,
    set_screw_angle=90.0,
    set_screw_head_depth=4.0,
)

class WallMountClamp:
    def __init__(self, wp, m):
        self.wp = wp
        self.m = m
        self.build()
    def build(self):
        m = self.m
        outer = (
            cq.Workplane("XY")
            .rect(m.outer_width, m.outer_height)
            .extrude(m.thickness)
        )
        inner = (
            cq.Workplane("XY")
            .rect(
                m.outer_width - 2*m.flange_thickness,
                m.outer_height - 2*m.web_thickness,
            )
            .extrude(m.thickness)
        )
        base = outer.cut(inner)
        base = base.edges("<X or >X or <Y or >Y").chamfer(m.chamfer)
        mount_face = base.faces("<Z")
        mount_holes = (
            mount_face
            .rarray(m.mount_hole_spacing, 0, 2, 1, center=True)
            .hole(m.mount_hole_dia)
        )
        set_screw_face = mount_holes.faces(">X")
        result = (
            set_screw_face
            .csk_face_hole(
                diameter=m.set_screw_hole_dia,
                csk_diameter=m.set_screw_head_dia,
                csk_angle=m.set_screw_angle,
                depth=m.set_screw_head_depth,
                offset=(0,0)
            )
        )
        self.model = result

result = WallMountClamp(cq.Workplane('XY'), measures).model
