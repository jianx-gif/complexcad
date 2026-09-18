import cadquery as cq

class Measures:
    def __init__(self):
        self.material_thickness = 10.0
        self.vertical_leg_height = 60.0
        self.horizontal_leg_length = 80.0
        self.leg_width = 10.0
        self.chamfer_size = 1.0
        self.hole_diameter = 6.0
        self.hole_positions = [(20.0, 5.0), (60.0, 5.0)]
        self.tslot_bottom_width = 8.0
        self.tslot_top_width = 20.0
        self.tslot_bottom_height = 24.0
        self.tslot_top_height = 6.0
        self.tslot_depth = 8.0
        self.tslot_offset_y = 30.0
        self.gusset_thickness = 10.0
        self.gusset_height = 15.0
        self.gusset_width = 20.0

class LBracketMount:
    def __init__(self, wp, measures):
        self.wp = wp
        self.m = measures
        self.model = None
        self.build()

    def build(self):
        m = self.m
        base = (
            self.wp
            .moveTo(0, 0)
            .lineTo(0, m.vertical_leg_height)
            .lineTo(m.leg_width, m.vertical_leg_height)
            .lineTo(m.leg_width, m.leg_width)
            .lineTo(m.horizontal_leg_length, m.leg_width)
            .lineTo(m.horizontal_leg_length, 0)
            .lineTo(0, 0)
            .close()
            .extrude(m.material_thickness)
        )
        base = base.edges("|Z").chamfer(m.chamfer_size)
        holes = (
            base
            .faces(">Z")
            .workplane()
            .pushPoints(m.hole_positions)
            .hole(m.hole_diameter)
        )
        tslot_base = (
            holes
            .faces(">X")
            .workplane()
            .center(0, m.tslot_offset_y)
            .rect(m.tslot_bottom_width, m.tslot_bottom_height + m.tslot_top_height)
            .cutBlind(m.tslot_depth)
        )
        top_center_y = m.tslot_offset_y + (m.tslot_bottom_height / 2) + (m.tslot_top_height / 2)
        tslot = (
            tslot_base
            .faces(">X")
            .workplane()
            .center(0, top_center_y)
            .rect(m.tslot_top_width, m.tslot_top_height)
            .cutBlind(m.tslot_depth)
        )
        gusset_shape = (
            cq.Workplane("XY")
            .moveTo(0, 0)
            .lineTo(m.leg_width, 0)
            .lineTo(0, m.leg_width)
            .close()
            .extrude(m.material_thickness)
        )
        final = tslot.union(gusset_shape)
        self.model = final

measures = Measures()
result = LBracketMount(cq.Workplane("XY"), measures).model
