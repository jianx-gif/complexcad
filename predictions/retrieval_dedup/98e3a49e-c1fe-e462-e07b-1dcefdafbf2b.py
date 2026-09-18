
import cadquery as cq

# Parameters
block_base_length = 80.0
block_base_width = 60.0
block_top_length = 50.0
block_top_width = 40.0
block_height = 90.0
section_count = 6
section_height = block_height / section_count
chamfer_distance = 2.0
hole_diameter = 4.0
hole_rows = 3
hole_cols = 4
hole_spacing_x = 12.0
hole_spacing_y = 12.0

class PowerDistributionBlock:
    def __init__(self):
        self.lengths = []
        self.widths = []
        self.build_profiles()
        self.result = None

    def build_profiles(self):
        for i in range(section_count + 1):
            t = i / section_count
            length = block_base_length * (1 - t) + block_top_length * t
            width = block_base_width * (1 - t) + block_top_width * t
            self.lengths.append(length)
            self.widths.append(width)

    def loft_body(self):
        # Start with first profile
        solid = cq.Workplane('XY').rect(self.lengths[0], self.widths[0])
        for i in range(1, len(self.lengths)):
            solid = solid.workplane(offset=i * section_height).rect(self.lengths[i], self.widths[i])
        solid = solid.loft()
        return solid

    def add_top_hole_grid(self, solid):
        points = []
        start_x = -((hole_cols - 1) * hole_spacing_x) / 2.0
        start_y = -((hole_rows - 1) * hole_spacing_y) / 2.0
        for col in range(hole_cols):
            for row in range(hole_rows):
                points.append((start_x + col * hole_spacing_x, start_y + row * hole_spacing_y))
        solid = solid.faces('>Z').workplane().pushPoints(points).hole(hole_diameter)
        return solid

    def apply_chamfer(self, solid):
        solid = solid.edges().chamfer(chamfer_distance)
        return solid

    def build(self):
        body = self.loft_body()
        body = self.add_top_hole_grid(body)
        body = self.apply_chamfer(body)
        self.result = body
        return body

block = PowerDistributionBlock()
result = block.build()
