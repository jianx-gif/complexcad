import cadquery as cq
import copy
from types import SimpleNamespace as Measures

def combine_wires(self):
    wires = [obj for obj in self.objects if isinstance(obj, cq.Wire)]
    if len(wires) < 2:
        return self
    temp = cq.Workplane('XY')
    for w in wires:
        temp = temp.add(w).toPending().extrude(0.01)
    combined = temp.combine()
    face = combined.faces(cq.DirectionMinMaxSelector(wires[0].normal(), directionMax=False)).first()
    return face.wires()

class FlatPlateXMount:
    def __init__(self, workplane, measures):
        cq.Workplane.combine_wires = combine_wires
        self.workplane = workplane
        self.measures = copy.deepcopy(measures)
        self.build()
    def build(self):
        m = self.measures
        base = (
            cq.Workplane('XY')
            .center(-0.5 * m.plate_width, -0.5 * m.plate_depth)
            .polyline([
                (0, 0),
                (m.plate_width, 0),
                (m.plate_width, m.plate_depth),
                (0, m.plate_depth),
                (0, 0)
            ])
            .close()
            .extrude(m.plate_thickness)
        )
        rib = (
            base.faces('<Z').workplane()
            .rect(m.rib_width, m.rib_length, centered=True)
            .extrude(m.rib_height)
        )
        # socket composite profile
        socket_profile = (
            cq.Workplane('XY')
            .center(-0.5 * m.socket_width, -0.5 * m.socket_depth)
            .polyline([
                (0, 0),
                (m.socket_width, 0),
                (m.socket_width, m.socket_depth),
                (0, m.socket_depth),
                (0, 0)
            ])
            .close()
            .add(
                cq.Workplane('XY')
                .center(-0.5 * m.socket_width + m.socket_notch_offset, -0.5 * m.socket_depth)
                .rect(m.socket_notch_width, m.socket_notch_depth)
            )
            .combine_wires()
            .toPending()
        )
        socket_cut = (
            socket_profile
            .extrude(-m.socket_recess_depth)
            .edges('>>Z')
            .fillet(m.socket_fillet)
        )
        plate_with_socket = rib.cut(socket_cut)
        # counterbore and through hole
        hole_wp = plate_with_socket.faces('>Z').workplane()
        plate_cb = hole_wp.center(* (m.hole_offset_x, m.hole_offset_y)).hole(m.counterbore_diameter, depth=m.counterbore_depth)
        plate_final = plate_cb.faces('>Z').workplane().center(* (m.hole_offset_x, m.hole_offset_y)).hole(m.through_hole_diameter, depth=m.plate_thickness)
        self.model = plate_final

m = Measures(
    plate_width = 80.0,
    plate_depth = 60.0,
    plate_thickness = 5.0,
    rib_width = 12.0,
    rib_length = 40.0,
    rib_height = 3.0,
    socket_width = 30.0,
    socket_depth = 20.0,
    socket_notch_width = 10.0,
    socket_notch_depth = 5.0,
    socket_notch_offset = 10.0,
    socket_recess_depth = 4.0,
    socket_fillet = 1.0,
    hole_offset_x = 20.0,
    hole_offset_y = 15.0,
    through_hole_diameter = 4.0,
    counterbore_diameter = 8.0,
    counterbore_depth = 2.0,
)

result = FlatPlateXMount(cq.Workplane('XY'), m).model