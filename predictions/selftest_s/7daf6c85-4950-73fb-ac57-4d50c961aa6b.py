import cadquery as cq

leg_length_long = 80.0
leg_length_short = 60.0
bracket_thickness = 8.0
leg_width = 20.0
inner_fillet_radius = 2.0
hex_radius = 6.0
hex_diameter = hex_radius * 2.0
clearance_hole_diameter = 4.0
hole_offset_x = 30.0
pattern_spacing = 15.0

class LBracket:
    def __init__(self):
        self.model = cq.Workplane('XY')
        self.build()

    def build(self):
        profile = (
            self.model
            .polyline([
                (0, 0),
                (leg_length_long, 0),
                (leg_length_long, leg_width),
                (leg_width, leg_width),
                (leg_width, leg_length_short + leg_width),
                (0, leg_length_short + leg_width),
                (0, 0)
            ])
            .close()
        )
        solid = profile.extrude(bracket_thickness)
        solid = solid.edges("|Z").fillet(inner_fillet_radius)
        hex_center_x = leg_width / 2.0
        hex_center_y = leg_width / 2.0
        solid = (
            solid
            .faces('>Z')
            .workplane()
            .center(hex_center_x, hex_center_y)
            .polygon(6, hex_diameter)
            .cutBlind(bracket_thickness)
        )
        hole_start_x = leg_length_long - hole_offset_x
        hole_start_y = leg_width / 2.0
        solid = (
            solid
            .faces('>Z')
            .workplane()
            .center(hole_start_x, hole_start_y)
            .rarray(pattern_spacing, pattern_spacing, 2, 2)
            .hole(clearance_hole_diameter)
        )
        self.model = solid

result = LBracket().model
