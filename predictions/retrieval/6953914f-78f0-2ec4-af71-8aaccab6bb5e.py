import cadquery as cq
import copy
import math
from types import SimpleNamespace as Measures

class XMountSocket:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = copy.deepcopy(measures)
        self.build()
    def build(self):
        m = self.measures
        outer_radius = 0.5 * m.overall_diameter
        inner_radius = outer_radius - m.wall_thickness
        profile = (
            cq.Workplane('XZ')
            .moveTo(outer_radius, 0)
            .lineTo(outer_radius, m.overall_height)
            .lineTo(inner_radius, m.overall_height)
            .lineTo(inner_radius, 0)
            .close()
        )
        shell = profile.revolve(360)
        shell = shell.edges('>Z').chamfer(m.chamfer)
        shell = (
            shell.faces('>Z')
            .workplane()
            .hole(m.blind_hole_diameter, m.blind_hole_depth)
        )
        slot_box = (
            cq.Workplane('XY')
            .box(m.wall_thickness + 0.2, m.slot_length, m.slot_width, centered=(True, False, True))
            .translate((inner_radius + m.wall_thickness/2, 0, m.slot_height))
        )
        slots_combined = cq.Workplane('XY')
        for i in range(m.slot_count):
            angle = i * 360.0 / m.slot_count
            slots_combined = slots_combined.union(slot_box.rotate((0,0,0), (0,0,1), angle))
        slots_solid = slots_combined.combine().val()
        shell = shell.cut(slots_solid)
        self.model = shell

measures = Measures(
    overall_diameter = 80.0,
    overall_height = 30.0,
    wall_thickness = 2.0,
    blind_hole_diameter = 12.0,
    blind_hole_depth = 10.0,
    slot_length = 4.0,
    slot_width = 2.0,
    slot_height = 15.0,
    slot_count = 8,
    chamfer = 0.8
)

result = XMountSocket(cq.Workplane('XY'), measures).model
