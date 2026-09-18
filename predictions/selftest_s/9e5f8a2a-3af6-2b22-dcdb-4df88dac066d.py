import cadquery as cq
import copy
from types import SimpleNamespace as Measures
from math import tan, radians

def combine_wires(self):
    wires = [obj for obj in self.objects if isinstance(obj, cq.Wire)]
    if len(wires) < 2:
        return self
    temp = cq.Workplane("XY")
    for w in wires:
        temp = temp.add(w).toPending().extrude(0.01)
    combined = temp.combine().faces(cq.DirectionMinMaxSelector(cq.Vector(0,0,1), directionMax=False)).wires()
    return combined

cq.Workplane.combine_wires = combine_wires

class ClutchDisc:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = copy.deepcopy(measures)
        self.build()

    def build(self):
        m = self.measures
        outer_rect = cq.Workplane("XY").rect(2*m.outer_radius, 2*m.outer_radius).wire()
        inner_hub = cq.Workplane("XY").circle(m.hub_radius).wire()
        base_profile = (
            cq.Workplane("XY")
            .add(outer_rect)
            .add(inner_hub)
            .combine_wires()
            .toPending()
            .extrude(m.base_thickness)
        )
        base_profile = base_profile.edges("|Z and >X and >Y").fillet(m.outer_fillet)
        socket_cyl = (
            cq.Workplane("XY")
            .circle(m.socket_diameter/2)
            .extrude(m.socket_depth)
        )
        cone_height = (m.socket_csk_diameter/2) / tan(radians(m.socket_csk_angle/2))
        socket_cone = (
            cq.Workplane("XY")
            .circle(m.socket_csk_diameter/2)
            .extrude(cone_height)
            .translate((0,0,m.socket_depth - cone_height))
        )
        socket = socket_cyl.union(socket_cone)
        friction_outer = cq.Workplane("XY").circle(m.friction_outer/2).extrude(m.friction_thickness)
        friction_inner = cq.Workplane("XY").circle(m.friction_inner/2).extrude(m.friction_thickness)
        friction_pocket = friction_outer.cut(friction_inner)
        friction_pocket = friction_pocket.edges("<Z").chamfer(m.friction_chamfer)
        vent_cyl = cq.Workplane("XY").circle(m.vent_diameter/2).extrude(m.friction_thickness)
        vent_pattern = vent_cyl
        for i in range(1, m.vent_count):
            angle = 360.0/m.vent_count * i
            vent_pattern = vent_pattern.union(
                vent_cyl.translate((m.friction_inner/2 + m.vent_spacing/2, 0, 0)).rotate((0,0,0), (0,0,1), angle)
            )
        friction_pocket = friction_pocket.cut(vent_pattern)
        bolt_cyl = cq.Workplane("XY").circle(m.bolt_diameter/2).extrude(m.base_thickness + 2)
        bolt_pattern = bolt_cyl
        for i in range(1, m.bolt_count):
            angle = 360.0/m.bolt_count * i
            bolt_pattern = bolt_pattern.union(
                bolt_cyl.translate((m.bolt_circle_radius, 0, 0)).rotate((0,0,0), (0,0,1), angle)
            )
        self.model = (
            base_profile
            .cut(socket)
            .cut(friction_pocket)
            .cut(bolt_pattern)
        )

measures = Measures(
    outer_radius = 45,
    hub_radius = 15,
    base_thickness = 5,
    outer_fillet = 2,
    socket_diameter = 12,
    socket_depth = 8,
    socket_csk_diameter = 16,
    socket_csk_angle = 60,
    friction_outer = 30,
    friction_inner = 20,
    friction_thickness = 2,
    friction_chamfer = 0.5,
    vent_diameter = 2,
    vent_spacing = 4,
    vent_count = 4,
    bolt_diameter = 4,
    bolt_count = 4,
    bolt_circle_radius = 18
)

result = ClutchDisc(cq.Workplane("XY"), measures).model