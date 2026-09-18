import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    outer_diameter = 40.0,
    wall_thickness = 3.0,
    height = 15.0,
    cam_width = 8.0,
    cam_radial_extra = 1.5,
    cam_depth = 2.0,
    entry_width = 6.0,
    entry_height = 5.0,
    chamfer_distance = 0.5,
    hole = Measures(
        diameter = 3.0,
        cbore_diameter = 5.0,
        cbore_depth = 3.0,
        positions = [(-10.0, 0), (10.0, 0)]
    )
)

class LidCatch:
    def __init__(self, measures):
        self.m = measures
        self.outer_radius = self.m.outer_diameter / 2.0
        self.inner_radius = self.outer_radius - self.m.wall_thickness

    def base_shell(self):
        outer = cq.Workplane('XY').circle(self.outer_radius).extrude(self.m.height)
        inner = cq.Workplane('XY').circle(self.inner_radius).extrude(self.m.height)
        return outer.cut(inner)

    def internal_cam(self, base):
        cam_radial = self.m.cam_depth + self.m.cam_radial_extra
        cam = (
            cq.Workplane('XY')
            .box(cam_radial, self.m.cam_width, self.m.height)
            .translate((self.inner_radius - self.m.cam_depth/2.0, 0, self.m.height/2.0))
        )
        return base.union(cam)

    def entry_slot(self, body):
        slot = (
            cq.Workplane('XY')
            .box(self.m.entry_width, self.m.entry_height, self.m.height)
            .translate((self.outer_radius - self.m.entry_width/2.0, 0, self.m.height/2.0))
        )
        cut_body = body.cut(slot)
        return cut_body.edges("|Z and >X").chamfer(self.m.chamfer_distance)

    def top_holes(self, part):
        return (
            part.faces('>Z')
            .workplane()
            .pushPoints(self.m.hole.positions)
            .cboreHole(self.m.hole.diameter, self.m.hole.cbore_diameter, self.m.hole.cbore_depth)
        )

    def build(self):
        shell = self.base_shell()
        shell_cam = self.internal_cam(shell)
        with_entry = self.entry_slot(shell_cam)
        final = self.top_holes(with_entry)
        return final

result = LidCatch(m).build()
