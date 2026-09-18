import cadquery as cq
from types import SimpleNamespace as Measures
import copy

def combine_wires(self):
    wires = [obj for obj in self.objects if isinstance(obj, cq.Wire)]
    if len(wires) < 2:
        return self
    temp = cq.Workplane('XY')
    for w in wires:
        temp = temp.add(w).toPending().extrude(0.01)
    combined = temp.combine().faces('>Z').wires()
    return combined

cq.Workplane.combine_wires = combine_wires

m = Measures(
    body = Measures(
        outer_diameter = 80.0,
        inner_diameter = 50.0,
        height = 30.0,
    ),
    groove = Measures(
        depth = 4.0,
        width = 20.0,
        radial_offset = 2.0,
    ),
    rim = Measures(
        chamfer = 2.0,
    ),
    mounting = Measures(
        hole_diameter = 5.0,
        hole_spacing = 40.0,
        hole_offset = 12.0,
    )
)

class XMountSocket:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = copy.deepcopy(measures)
        self.build()

    def build(self):
        m = self.measures
        body = (
            cq.Workplane('XY')
            .circle(m.body.outer_diameter/2)
            .circle(m.body.inner_diameter/2)
            .extrude(m.body.height)
        )
        groove_cut = (
            cq.Workplane('XY')
            .rect(m.groove.width, m.groove.depth)
            .translate((m.body.inner_diameter/2 + m.groove.radial_offset + m.groove.width/2, 0))
            .extrude(m.body.height)
        )
        body = body.cut(groove_cut)
        body = body.edges('>Z').chamfer(m.rim.chamfer)
        # Mounting holes on top face
        body = (
            body
            .faces('>Z')
            .workplane()
            .pushPoints([
                ( m.mounting.hole_spacing/2,  m.mounting.hole_offset),
                (-m.mounting.hole_spacing/2,  m.mounting.hole_offset),
                ( m.mounting.hole_spacing/2, -m.mounting.hole_offset),
                (-m.mounting.hole_spacing/2, -m.mounting.hole_offset),
            ])
            .hole(m.mounting.hole_diameter)
        )
        self.model = body

result = XMountSocket(cq.Workplane('XY'), m).model
