
import cadquery as cq

class Measures:
    def __init__(self):
        self.vertical_leg_length = 80.0
        self.horizontal_leg_length = 60.0
        self.leg_width = 30.0
        self.material_thickness = 8.0
        self.rib_thickness = 5.0
        self.rib_offset = 2.0
        self.pocket_width = 20.0
        self.pocket_length = 40.0
        self.pocket_depth = 5.0
        self.hole_diameter = 5.0
        self.hole_spacing_y = 12.0
        self.hole_spacing_x = 12.0
        self.hole_rows = 3
        self.hole_cols = 2
        self.hole_offset_y = 10.0
        self.hole_offset_x = 0.0

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        # Base vertical leg
        vertical = cq.Workplane("XY").box(m.leg_width, m.vertical_leg_length, m.material_thickness)
        # Horizontal leg positioned at top of vertical leg
        horiz_center_x = m.horizontal_leg_length/2 + m.leg_width/2
        horiz_center_y = m.vertical_leg_length/2 - m.leg_width/2
        horizontal = cq.Workplane("XY").box(m.horizontal_leg_length, m.leg_width, m.material_thickness)
        horizontal = horizontal.translate((horiz_center_x, horiz_center_y, 0))
        base = vertical.union(horizontal)
        # Reinforced inner rib inside L corner
        rib_length = m.vertical_leg_length - 2*m.rib_offset
        rib = cq.Workplane("XY").box(m.rib_thickness, rib_length, m.material_thickness)
        rib = rib.translate((-(m.leg_width/2 - m.rib_thickness/2), m.rib_offset - m.vertical_leg_length/2 + rib_length/2, 0))
        base = base.union(rib)
        # Recessed pocket on horizontal leg
        pocket = (
            base.faces('>Z')
            .workplane(centerOption='CenterOfBoundBox')
            .center(m.horizontal_leg_length/2 - m.pocket_length/2 - 5, m.vertical_leg_length/2 - m.leg_width/2)
            .rect(m.pocket_width, m.pocket_length)
            .cutBlind(-m.pocket_depth)
        )
        # Clearance holes pattern on vertical leg
        holes = (
            pocket.faces('>Z')
            .workplane(centerOption='CenterOfBoundBox')
            .center(-m.leg_width/4, -m.vertical_leg_length/2 + m.hole_offset_y)
            .rarray(m.hole_spacing_x, m.hole_spacing_y, m.hole_cols, m.hole_rows)
            .hole(m.hole_diameter)
        )
        self.model = holes

measures = Measures()
result = LBracket(cq.Workplane("XY"), measures).model
