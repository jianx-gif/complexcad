import cadquery as cq
import math
from types import SimpleNamespace as Measures

params = Measures(
    outer_radius=30.0,
    inner_radius=15.0,
    height=60.0,
    wall_thickness=10.0,
    chamfer=0.8,
    vent_slot_width=12.0,
    vent_slot_height=30.0,
    rib_thickness=2.0,
    rib_height=5.0,
    rib_count=4,
    hole_diameter=5.0,
    hole_angle_offset=0.0,
    hole_spacing_angle=120.0,
    hole_center_height=45.0,
)

class SoundSensorEnclosure:
    def __init__(self, wp, measures):
        self.wp = wp
        self.m = measures
        self.build()
        self.model = self.solid

    def build(self):
        m = self.m
        profile = (
            cq.Workplane('XZ')
            .moveTo(m.outer_radius, 0)
            .lineTo(m.outer_radius, m.height)
            .lineTo(m.inner_radius, m.height)
            .lineTo(m.inner_radius, 0)
            .close()
        )
        solid = profile.revolve()
        solid = solid.edges('>Z').chamfer(m.chamfer)
        # vent pocket on outer surface
        vent = (
            cq.Workplane('XY')
            .box(m.wall_thickness, m.vent_slot_width, m.vent_slot_height)
            .translate((m.outer_radius - m.wall_thickness/2, 0, m.height/2))
        )
        solid = solid.cut(vent)
        rib = (
            cq.Workplane('XY')
            .box(m.rib_thickness, m.rib_height, m.wall_thickness)
            .translate((m.inner_radius - m.rib_thickness/2 + 0.5, 0, m.height/2))
        )
        ribs = rib
        for i in range(1, m.rib_count):
            angle = 360.0 / m.rib_count * i
            ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))
        solid = solid.union(ribs)
        hole = cq.Workplane('XY').circle(m.hole_diameter/2).extrude(m.wall_thickness + 2)
        for i in range(3):
            angle = m.hole_angle_offset + i * m.hole_spacing_angle
            rad = m.inner_radius + m.wall_thickness/2
            x = rad * math.cos(math.radians(angle))
            y = rad * math.sin(math.radians(angle))
            solid = solid.cut(hole.translate((x, y, m.hole_center_height)))
        self.solid = solid

enclosure = SoundSensorEnclosure(cq.Workplane('XY'), params)
result = enclosure.model
