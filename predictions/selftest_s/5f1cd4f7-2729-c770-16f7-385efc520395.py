import cadquery as cq

# Parameters
total_length = 80.0
start_width = 45.0
end_width = 15.0
profile_depth = 20.0
wall_thickness = 3.0
section_count = 6
section_height = total_length / (section_count - 1)
fillet_radius = 1.0
groove_width = 30.0
groove_depth = 5.0

class LoftedTaperedComponent:
    def __init__(self, total_length, start_width, end_width, profile_depth, wall_thickness, section_height, section_count):
        self.total_length = total_length
        self.start_width = start_width
        self.end_width = end_width
        self.profile_depth = profile_depth
        self.wall_thickness = wall_thickness
        self.section_height = section_height
        self.section_count = section_count

    def _width_at_height(self, height):
        return self.start_width - (self.start_width - self.end_width) * (height / self.total_length)

    def _generate_widths(self):
        return [self._width_at_height(i * self.section_height) for i in range(self.section_count)]

    def build_outer_loft(self):
        widths = self._generate_widths()
        solid = (
            cq.Workplane('XY')
            .rect(widths[0], self.profile_depth)
            .workplane(offset=self.section_height)
            .rect(widths[1], self.profile_depth)
            .loft(combine=True)
        )
        for i in range(1, len(widths) - 1):
            solid = (
                solid.faces('>Z')
                .workplane()
                .rect(widths[i], self.profile_depth)
                .workplane(offset=self.section_height)
                .rect(widths[i + 1], self.profile_depth)
                .loft(combine=True)
            )
        return solid

    def build_inner_loft(self):
        inner_start_w = self.start_width - 2 * self.wall_thickness
        inner_end_w = self.end_width - 2 * self.wall_thickness
        inner_depth = self.profile_depth - 2 * self.wall_thickness
        inner_widths = [inner_start_w - (inner_start_w - inner_end_w) * (i / (self.section_count - 1)) for i in range(self.section_count)]
        solid = (
            cq.Workplane('XY')
            .rect(inner_widths[0], inner_depth)
            .workplane(offset=self.section_height)
            .rect(inner_widths[1], inner_depth)
            .loft(combine=True)
        )
        for i in range(1, len(inner_widths) - 1):
            solid = (
                solid.faces('>Z')
                .workplane()
                .rect(inner_widths[i], inner_depth)
                .workplane(offset=self.section_height)
                .rect(inner_widths[i + 1], inner_depth)
                .loft(combine=True)
            )
        return solid

    def assemble(self):
        outer = self.build_outer_loft()
        outer = outer.edges().fillet(fillet_radius)
        inner = self.build_inner_loft()
        solid = outer.cut(inner)
        groove_plane = solid.faces('>Z').workplane(centerOption='CenterOfBoundBox')
        solid = groove_plane.center(0, 0).rect(groove_width, self.profile_depth - self.wall_thickness).cutBlind(-groove_depth)
        return solid

component = LoftedTaperedComponent(total_length, start_width, end_width, profile_depth, wall_thickness, section_height, section_count)
result = component.assemble()
