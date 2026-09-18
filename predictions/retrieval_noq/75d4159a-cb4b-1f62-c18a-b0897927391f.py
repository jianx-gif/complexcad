import cadquery as cq
from types import SimpleNamespace as Measures

class WallMountCradle:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = measures
        self.build()
    def build(self):
        m = self.measures
        base = (
            cq.Workplane('XZ')
            .rect(m.base_width, m.base_height)
            .extrude(m.base_depth)
        )
        channel = (
            base
            .faces('>Y')
            .workplane()
            .polyline([
                (-m.channel_width/2, m.base_height/2),
                (-m.channel_width/2, m.base_height/2 - m.channel_height),
                ( m.channel_width/2, m.base_height/2 - m.channel_height),
                ( m.channel_width/2, m.base_height/2)
            ])
            .close()
            .cutBlind(m.channel_length)
        )
        drilled = (
            channel
            .faces('>Y')
            .workplane()
            .center(0, m.base_height/2 - m.channel_height/2)
            .cboreHole(m.sensor_diameter, m.sensor_counterbore_dia, m.sensor_counterbore_depth)
        )
        self.model = (
            drilled
            .edges('|Z')
            .chamfer(m.chamfer)
        )

m = Measures(
    base_width = 80.0,
    base_height = 50.0,
    base_depth = 15.0,
    channel_width = 40.0,
    channel_height = 20.0,
    channel_length = 10.0,
    sensor_diameter = 5.0,
    sensor_counterbore_dia = 9.0,
    sensor_counterbore_depth = 4.0,
    chamfer = 0.8
)

result = WallMountCradle(cq.Workplane('XY'), m).model