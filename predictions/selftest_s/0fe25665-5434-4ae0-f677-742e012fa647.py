import cadquery as cq
import copy
import math
from types import SimpleNamespace as Measures

def csk_hole(workplane, diameter, csk_diameter, csk_angle, depth=None, offset=(0,0)):
    ctx = workplane.findSolid()
    if depth is None:
        depth = workplane.largestDimension()
    for face in workplane.objects:
        if isinstance(face, cq.Face):
            origin = face.Center()
            normal = face.normalAt()
            if normal.normalized() == cq.Vector(0,0,1):
                x_dir = cq.Vector(1,0,0)
            elif normal.normalized() == cq.Vector(0,0,-1):
                x_dir = cq.Vector(-1,0,0)
            else:
                x_dir = cq.Vector(0,0,1).cross(normal)
            plane = cq.Plane(origin, x_dir, normal)
            plane.setOrigin2d(*offset)
            bore_dir = normal.multiply(-1)
            center = plane.toWorldCoords((0,0,0))
            hole = cq.Solid.makeCylinder(0.5*diameter, depth, center, bore_dir)
            csk_radius = 0.5*csk_diameter
            csk_height = csk_radius / math.tan(math.radians(0.5*csk_angle))
            csk = cq.Solid.makeCone(csk_radius, 0.0, csk_height, center, bore_dir)
            csk_hole = hole.fuse(csk)
            ctx = ctx.cut(csk_hole)
    return workplane.newObject([ctx])

class XMountSocket:
    def __init__(self, wp, measures):
        self.workplane = wp
        self.measures = copy.deepcopy(measures)
        self.build()

    def build(self):
        m = self.measures
        base = (cq.Workplane('XY')
                .circle(m.outer_radius)
                .extrude(m.base_thickness)
                .edges('<Z')
                .chamfer(m.base_fillet_radius))
        body = (cq.Workplane('XY')
                .circle(m.outer_radius)
                .extrude(m.body_height))
        flange = (cq.Workplane('XY')
                .circle(m.flange_radius)
                .extrude(m.flange_thickness)
                .translate((0,0,m.base_thickness + m.body_height)))
        shell = base.union(body).union(flange)
        inner = (cq.Workplane('XY')
                .circle(m.inner_radius)
                .extrude(m.total_height))
        shell = shell.cut(inner)
        rib_thickness = m.outer_radius - m.inner_radius
        rib = (cq.Workplane('XY')
                .box(rib_thickness, 6.0, m.body_height)
                .translate((m.inner_radius + rib_thickness/2, 0, m.base_thickness + m.body_height/2)))
        shell = shell.union(rib)
        face_wp = cq.Workplane('XY').add(shell).faces('>Z')
        shell = csk_hole(face_wp, m.counter_sink_diameter, m.counter_sink_diameter, m.counter_sink_angle, depth=m.flange_thickness).objects[0]
        self.model = self.workplane.newObject([shell])

m = Measures(
    outer_radius = 30.0,
    inner_radius = 25.0,
    base_thickness = 5.0,
    body_height = 40.0,
    flange_radius = 35.0,
    flange_thickness = 8.0,
    base_fillet_radius = 2.0,
    counter_sink_diameter = 6.0,
    counter_sink_angle = 90,
)

m.total_height = m.base_thickness + m.body_height + m.flange_thickness

socket = XMountSocket(cq.Workplane('XY'), m)
result = socket.model
