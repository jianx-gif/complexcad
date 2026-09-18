import cadquery as cq
import copy
from types import SimpleNamespace as Measures

def combine_wires(self):
    wires = [obj for obj in self.objects if isinstance(obj, cq.Wire)]
    if len(wires) < 2:
        return self
    extrude_direction = wires[0].normal()
    solids = (
        cq.Workplane("XY")
        .add(cq.Face.makeFromWires(wires[0]))
        .workplane()
    )
    for wire in wires:
        solids = solids.add(wire).toPending().extrude(1)
    combined_wire = (
        solids
        .combine()
        .faces(cq.DirectionMinMaxSelector(extrude_direction, directionMax=False))
        .wires()
    )
    return combined_wire

class XMountSocket:
    def __init__(self, workplane, measures):
        cq.Workplane.combine_wires = combine_wires
        self.workplane = workplane
        self.measures = copy.deepcopy(measures)
        self.build()

    def build(self):
        m = self.measures
        # Outer block with side cable notch
        outer = (
            cq.Workplane("XY")
            .center(-0.5 * m.outer_width, -0.5 * m.outer_depth)
            .polyline([
                (0, 0),
                (m.outer_width, 0),
                (m.outer_width, m.outer_depth),
                (0, m.outer_depth),
                (0, 0)
            ])
            .close()
            .add(
                cq.Workplane("XY")
                .center(-0.5 * m.outer_width + m.wall_thickness, -0.5 * m.outer_depth + m.notch_offset)
                .rect(m.notch_width, m.notch_depth, centered=False, forConstruction=True)
            )
            .combine_wires()
            .toPending()
            .extrude(m.total_height)
        )
        # Inner socket cavity
        cavity = (
            cq.Workplane("XY")
            .center(-0.5 * m.inner_width, -0.5 * m.inner_depth)
            .rect(m.inner_width, m.inner_depth)
            .extrude(m.socket_height)
        )
        # Boss protrusion on bottom side
        boss = (
            cq.Workplane("XY")
            .center(0, 0)
            .circle(m.boss_diameter / 2)
            .extrude(m.boss_height)
            .translate((0, 0, -m.boss_height))
        )
        # Assemble base geometry
        base = outer.cut(cavity).union(boss)
        # Drill four through holes (2x2 grid) through entire part
        hole_grid = (
            base
            .faces(">Z")
            .workplane()
            .pushPoints([
                (-m.hole_spacing/2, -m.hole_spacing/2),
                ( m.hole_spacing/2, -m.hole_spacing/2),
                (-m.hole_spacing/2,  m.hole_spacing/2),
                ( m.hole_spacing/2,  m.hole_spacing/2)
            ])
            .hole(m.hole_diameter)
        )
        # Apply chamfer to external edges
        result_part = (
            hole_grid
            .edges("<Z")
            .chamfer(m.chamfer)
        )
        self.model = result_part

measures = Measures(
    outer_width = 60.0,
    outer_depth = 40.0,
    total_height = 20.0,
    wall_thickness = 5.0,
    notch_width = 8.0,
    notch_depth = 4.0,
    notch_offset = 12.0,
    inner_width = 50.0,
    inner_depth = 30.0,
    socket_height = 12.0,
    boss_diameter = 12.0,
    boss_height = 4.0,
    hole_diameter = 1.0,
    hole_spacing = 15.0,
    chamfer = 2.0,
)

result = XMountSocket(cq.Workplane("XY"), measures).model