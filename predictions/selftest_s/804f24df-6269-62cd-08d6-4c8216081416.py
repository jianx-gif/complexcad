import cadquery as cq

class Measures:
    def __init__(self):
        self.leg_length = 70.0
        self.arm_length = 60.0
        self.leg_width = 30.0
        self.arm_width = 30.0
        self.leg_thickness = 30.0
        self.extra_thickness = 45.0
        self.base_extension = 30.0
        self.chamfer_size = 10.0
        self.hole_diameter = 5.0
        self.cbore_diameter = 7.5
        self.cbore_depth = 4.0
        self.hole_spacing = 30.0
        self.hole_row_offset = 20.0

class LSupportBracket:
    def __init__(self, workplane, measures):
        self.wp = workplane
        self.m = measures
        self.model = None
        self.build()

    def build(self):
        m = self.m
        profile = (
            self.wp
            .moveTo(0, 0)
            .lineTo(m.leg_width, 0)
            .lineTo(m.leg_width, m.leg_length)
            .lineTo(m.leg_width + m.base_extension, m.leg_length)
            .lineTo(m.leg_width + m.base_extension, m.leg_length + m.base_extension)
            .lineTo(0, m.leg_length + m.base_extension)
            .close()
        )
        base = profile.extrude(m.leg_thickness)
        extra = (
            cq.Workplane("XY")
            .center(m.leg_width + m.base_extension/2, m.leg_length + m.base_extension/2)
            .rect(m.base_extension, m.base_extension)
            .extrude(m.extra_thickness - m.leg_thickness)
        )
        bracket = base.union(extra)
        bracket = (
            bracket.faces(">X").edges().chamfer(m.chamfer_size)
            .faces("<X").edges().chamfer(m.chamfer_size)
            .faces(">Y").edges().chamfer(m.chamfer_size)
        )
        holes = (
            bracket.faces(">Z")
            .workplane(centerOption='CenterOfBoundBox')
            .move(m.leg_width + m.base_extension/2, m.leg_length + m.base_extension/2 + m.hole_row_offset)
            .rect(m.hole_spacing, m.hole_spacing, forConstruction=True)
            .vertices()
            .cboreHole(m.hole_diameter, m.cbore_diameter, m.cbore_depth)
        )
        self.model = holes

measures = Measures()
result = LSupportBracket(cq.Workplane('XY'), measures).model
