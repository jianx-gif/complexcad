import cadquery as cq
import copy
from types import SimpleNamespace as Measures

def combine_wires(self):
    wires = [obj for obj in self.objects if isinstance(obj, cq.Wire)]
    if len(wires) < 2:
        return self
    temp = cq.Workplane("XY")
    for w in wires:
        temp = temp.add(w).toPending().extrude(0.01)
    combined = temp.combine().faces("<Z").wires()
    return combined

cq.Workplane.combine_wires = combine_wires

class RoverArmJoint:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = copy.deepcopy(measures)
        self.build()

    def build(self):
        m = self.measures
        base = (
            cq.Workplane("XY")
            .center(-0.5 * m.base_width, -0.5 * m.base_depth)
            .polyline([
                (0, 0),
                (m.base_width, 0),
                (m.base_width, m.base_depth),
                (0, m.base_depth)
            ])
            .close()
            .extrude(m.base_thickness)
            .edges("<Z and (|X or |Y)")
            .chamfer(m.edge_chamfer)
        )
        base = (
            base.faces("+Z")
            .workplane()
            .center(-0.5 * m.base_width + m.hole_offset_x, -0.5 * m.base_depth + m.hole_offset_y)
            .rarray(m.hole_spacing_x, m.hole_spacing_y, m.hole_cols, m.hole_rows)
            .hole(m.hole_diameter)
        )
        rib = (
            cq.Workplane("XY")
            .center(0, 0)
            .rect(m.rib_width, m.rib_depth)
            .extrude(m.rib_height)
            .translate((0, 0, m.base_thickness))
        )
        base = base.union(rib)
        outer_wire = (
            cq.Workplane("XY")
            .center(-0.5 * m.socket_width, -0.5 * m.socket_depth)
            .polyline([
                (0, 0),
                (m.socket_width, 0),
                (m.socket_width, m.socket_depth),
                (0, m.socket_depth)
            ])
            .close()
        )
        inner_wire = (
            cq.Workplane("XY")
            .center(-0.5 * m.socket_width, -0.5 * m.socket_depth)
            .polyline([
                (m.bevel, m.bevel),
                (m.socket_width - m.bevel, m.bevel),
                (m.socket_width - m.bevel, m.socket_depth - m.bevel),
                (m.bevel, m.socket_depth - m.bevel)
            ])
            .close()
        )
        socket = (
            cq.Workplane("XY")
            .add(outer_wire)
            .add(inner_wire)
            .combine_wires()
            .toPending()
            .extrude(m.socket_height)
            .edges("<Z")
            .chamfer(m.socket_chamfer)
            .translate((0, 0, m.base_thickness))
        )
        self.model = base.union(socket)

measures = Measures(
    base_width = 80.0,
    base_depth = 40.0,
    base_thickness = 6.0,
    rib_width = 30.0,
    rib_depth = 15.0,
    rib_height = 4.0,
    edge_chamfer = 1.0,
    hole_diameter = 5.0,
    hole_offset_x = 15.0,
    hole_offset_y = 10.0,
    hole_spacing_x = 30.0,
    hole_spacing_y = 15.0,
    hole_cols = 2,
    hole_rows = 2,
    socket_width = 30.0,
    socket_depth = 30.0,
    socket_height = 12.0,
    socket_chamfer = 0.8,
    bevel = 2.0,
)

result = RoverArmJoint(cq.Workplane("XY"), measures).model
