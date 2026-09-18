
import cadquery as cq
from dataclasses import dataclass

@dataclass
class Measures:
    vertical_leg_height: float = 80.0
    vertical_leg_width: float = 15.0
    horizontal_leg_length: float = 70.0
    horizontal_leg_width: float = 12.0
    step_extra_thickness: float = 6.0
    step_length: float = 30.0
    thickness: float = 8.0
    chamfer: float = 1.0
    hole_clearance: float = 5.0
    hole_cbore_diameter: float = 7.0
    hole_cbore_depth: float = 3.0
    hole_spacing: float = 20.0
    hole_offset_from_end: float = 20.0
    holes_per_leg: int = 3
    cable_slot_width: float = 8.0
    cable_slot_height: float = 20.0

class LBracketMount:
    def __init__(self, measures: Measures):
        self.m = measures
        self.model = cq.Workplane('XY')
        self.build()
        self.apply_chamfer()
        self.add_holes()
        self.result = self.model

    def build(self):
        m = self.m
        vertical = (
            cq.Workplane('XY')
            .rect(m.vertical_leg_width, m.vertical_leg_height)
            .extrude(m.thickness)
        )
        horizontal = (
            cq.Workplane('XY')
            .rect(m.horizontal_leg_length, m.horizontal_leg_width)
            .extrude(m.thickness)
            .translate((m.horizontal_leg_length/2, -m.vertical_leg_width/2, 0))
        )
        step = (
            cq.Workplane('XY')
            .rect(m.step_length, m.horizontal_leg_width + m.step_extra_thickness)
            .extrude(m.thickness)
            .translate((m.step_length/2, -(m.vertical_leg_width/2 + m.step_extra_thickness/2), 0))
        )
        slot = (
            cq.Workplane('XY')
            .rect(m.cable_slot_width, m.cable_slot_height)
            .extrude(m.thickness + 1)
            .translate((0, m.vertical_leg_height/2 - m.cable_slot_height/2, -0.5))
        )
        self.model = vertical.union(horizontal).union(step).cut(slot)

    def apply_chamfer(self):
        m = self.m
        self.model = self.model.edges().chamfer(m.chamfer)

    def add_holes(self):
        m = self.m
        # vertical leg holes
        self.model = (
            self.model.faces('>Z').workplane()
            .center(-m.vertical_leg_width/2, m.vertical_leg_height/2 - m.hole_offset_from_end)
            .rect(m.vertical_leg_width, m.hole_spacing * (m.holes_per_leg - 1))
            .vertices()
            .cboreHole(m.hole_clearance, m.hole_cbore_diameter, m.hole_cbore_depth)
        )
        # horizontal leg holes
        self.model = (
            self.model.faces('>Z').workplane()
            .center(m.horizontal_leg_length/2 - m.hole_offset_from_end, -m.horizontal_leg_width/2)
            .rect(m.hole_spacing * (m.holes_per_leg - 1), m.horizontal_leg_width)
            .vertices()
            .cboreHole(m.hole_clearance, m.hole_cbore_diameter, m.hole_cbore_depth)
        )

result = LBracketMount(Measures()).result
