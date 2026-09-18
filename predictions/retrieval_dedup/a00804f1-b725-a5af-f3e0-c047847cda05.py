import cadquery as cq
from types import SimpleNamespace as Measures
import math

class ReedSwitchHolder:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        outer = (
            cq.Workplane("XY")
            .rect(m.outer_width, m.outer_height)
            .extrude(m.depth)
        )
        inner = (
            cq.Workplane("XY")
            .rect(m.outer_width - 2*m.wall_thickness,
                  m.outer_height - 2*m.wall_thickness)
            .extrude(m.depth - m.base_thickness)
            .translate((0, 0, m.base_thickness))
        )
        shell = outer.cut(inner).val()
        recess = (
            cq.Workplane("XY")
            .rect(m.recess_width, m.recess_height)
            .extrude(m.recess_depth)
            .translate((0, 0, m.base_thickness + m.recess_offset_z))
        )
        vent_z_positions = [
            m.base_thickness + 5 + i * m.vent_spacing for i in range(m.vent_count)
        ]
        for z in vent_z_positions:
            slot_plus = (
                cq.Workplane("XZ")
                .rect(m.vent_slot_width, m.vent_slot_length)
                .extrude(m.wall_thickness + 0.2)
                .translate((0,
                          m.outer_height/2 - m.wall_thickness/2,
                          z))
                .val()
            )
            shell = shell.cut(slot_plus)
            slot_minus = (
                cq.Workplane("XZ")
                .rect(m.vent_slot_width, m.vent_slot_length)
                .extrude(m.wall_thickness + 0.2)
                .translate((0,
                          -m.outer_height/2 + m.wall_thickness/2,
                          z))
                .val()
            )
            shell = shell.cut(slot_minus)
        hole_coords = [
            (-m.outer_width/2 + m.mount_margin, -m.outer_height/2 + m.mount_margin),
            ( m.outer_width/2 - m.mount_margin, -m.outer_height/2 + m.mount_margin),
            (-m.outer_width/2 + m.mount_margin,  m.outer_height/2 - m.mount_margin),
            ( m.outer_width/2 - m.mount_margin,  m.outer_height/2 - m.mount_margin),
        ]
        holes = (
            cq.Workplane(obj=shell)
            .faces("<Z")
            .workplane()
            .pushPoints(hole_coords)
            .hole(m.mount_hole_diameter)
        )
        base = holes.cut(recess)
        corner_edges_selector = "((>X and >Y) or (<X and >Y) or (>X and <Y) or (<X and <Y))"
        result = base.edges(corner_edges_selector).chamfer(m.edge_chamfer)
        self.model = result

measures = Measures(
    outer_width = 80.0,
    outer_height = 40.0,
    depth = 30.0,
    wall_thickness = 4.0,
    base_thickness = 2.0,
    mount_margin = 10.0,
    mount_hole_diameter = 5.0,
    recess_width = 30.0,
    recess_height = 20.0,
    recess_depth = 8.0,
    recess_offset_z = 5.0,
    vent_slot_width = 2.0,
    vent_slot_length = 12.0,
    vent_spacing = 5.0,
    vent_count = 4,
    edge_chamfer = 1.0,
)

holder = ReedSwitchHolder(cq.Workplane("XY"), measures)
result = holder.model