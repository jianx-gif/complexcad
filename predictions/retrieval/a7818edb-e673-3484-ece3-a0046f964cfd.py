import cadquery as cq
import math

frame_width = 80.0
frame_height = 90.0
frame_thickness = 5.0
rib_height = 3.0
rib_thickness = 2.0  # not used directly, rib will be a ring with same wall thickness
chamfer_size = 0.5
mount_hole_diameter = 4.0
mount_hole_spacing = 35.0
threaded_insert_diameter = 5.0
threaded_insert_head_diameter = 8.0
threaded_insert_head_angle = 90.0
pattern_rows = 2
pattern_cols = 3
pattern_spacing_x = 20.0
pattern_spacing_y = 25.0


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

class WallMountFrame:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = measures
        self.build()
    def build(self):
        m = self.measures
        outer = (
            cq.Workplane("XY")
            .rect(m.frame_width, m.frame_height)
            .extrude(m.frame_thickness)
        )
        inner = (
            cq.Workplane("XY")
            .rect(m.frame_width - 2*m.frame_thickness, m.frame_height - 2*m.frame_thickness)
            .extrude(m.frame_thickness)
        )
        frame_body = outer.cut(inner)
        rib_ring = (
            cq.Workplane("XY")
            .rect(m.frame_width, m.frame_height)
            .rect(m.frame_width - 2*m.frame_thickness, m.frame_height - 2*m.frame_thickness)
            .extrude(m.rib_height)
            .translate((0, 0, m.frame_thickness))
        )
        base = frame_body.union(rib_ring)
        # mount holes on side face (+X)
        side_holes = (
            base
            .faces(">X")
            .workplane()
            .center(0, -m.mount_hole_spacing/2)
            .hole(m.mount_hole_diameter)
            .center(0, m.mount_hole_spacing)
            .hole(m.mount_hole_diameter)
        )
        # threaded insert pattern on front face (+Z)
        insert_grid = (
            side_holes
            .faces(">Z")
            .workplane()
            .rarray(m.pattern_spacing_x, m.pattern_spacing_y, m.pattern_cols, m.pattern_rows, center=True)
            .csk_face_hole(
                diameter=m.threaded_insert_diameter,
                csk_diameter=m.threaded_insert_head_diameter,
                csk_angle=m.threaded_insert_head_angle,
                offset=(0,0)
            )
        )
        result_model = (
            insert_grid
            .edges("|Z")
            .chamfer(m.chamfer_size)
        )
        self.model = result_model

measures = type('M', (), {
    'frame_width': frame_width,
    'frame_height': frame_height,
    'frame_thickness': frame_thickness,
    'rib_height': rib_height,
    'chamfer_size': chamfer_size,
    'mount_hole_diameter': mount_hole_diameter,
    'mount_hole_spacing': mount_hole_spacing,
    'threaded_insert_diameter': threaded_insert_diameter,
    'threaded_insert_head_diameter': threaded_insert_head_diameter,
    'threaded_insert_head_angle': threaded_insert_head_angle,
    'pattern_rows': pattern_rows,
    'pattern_cols': pattern_cols,
    'pattern_spacing_x': pattern_spacing_x,
    'pattern_spacing_y': pattern_spacing_y,
})

result = WallMountFrame(cq.Workplane("XY"), measures).model
