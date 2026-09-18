import cadquery as cq
from cadquery import selectors as s

# Parameters
block_length = 80.0
block_width = 40.0
block_thickness = 12.0
slot_width = 12.0
slot_height = 6.0
slot_offset_x = 0.0
slot_offset_y = 0.0
corner_fillet_radius = 2.0
pin_hole_diameter = 4.0
pin_hole_offset = 20.0
rib_thickness = 2.0
rib_height = 6.0
rib_spacing = 20.0
edge_chamfer = 1.0

class EjectorSpringRetainer:
    def __init__(self):
        self.block_length = block_length
        self.block_width = block_width
        self.block_thickness = block_thickness
        self.slot_width = slot_width
        self.slot_height = slot_height
        self.slot_offset_x = slot_offset_x
        self.slot_offset_y = slot_offset_y
        self.corner_fillet_radius = corner_fillet_radius
        self.pin_hole_diameter = pin_hole_diameter
        self.pin_hole_offset = pin_hole_offset
        self.rib_thickness = rib_thickness
        self.rib_height = rib_height
        self.rib_spacing = rib_spacing
        self.edge_chamfer = edge_chamfer

    def create_base(self):
        return (
            cq.Workplane("XY")
            .box(self.block_length, self.block_width, self.block_thickness, centered=(True, True, False))
        )

    def chamfer_edges(self, solid):
        return solid.edges("|Z").chamfer(self.edge_chamfer)

    def cut_slot(self, solid):
        return (
            solid.faces(">Z")
            .workplane()
            .center(self.slot_offset_x, self.slot_offset_y)
            .rect(self.slot_width, self.slot_height)
            .cutBlind(-self.block_thickness)
        )

    def add_fillet_to_slot_corners(self, solid):
        selector = s.BoxSelector(
            (-self.slot_width/2-0.1, -self.slot_height/2-0.1, -self.block_thickness-0.1),
            (self.slot_width/2+0.1, self.slot_height/2+0.1, 0.1)
        )
        return solid.edges(selector).fillet(self.corner_fillet_radius)

    def drill_pin_hole(self, solid):
        positions = [(self.pin_hole_offset, 0), (-self.pin_hole_offset, 0)]
        return (
            solid.faces("<Z")
            .workplane()
            .pushPoints(positions)
            .hole(self.pin_hole_diameter)
        )

    def add_ribs(self, solid):
        rib_count = int((self.block_length - self.rib_spacing) // self.rib_spacing)
        x_positions = [-(self.block_length/2) + self.rib_spacing/2 + i*self.rib_spacing for i in range(rib_count)]
        ribs = (
            cq.Workplane("XY", origin=(0, 0, self.block_thickness))
            .pushPoints([(x, 0) for x in x_positions])
            .rect(self.rib_thickness, self.block_width - 2*self.edge_chamfer)
            .extrude(self.rib_height)
        )
        return solid.union(ribs)

    def build(self):
        solid = self.create_base()
        solid = self.chamfer_edges(solid)
        solid = self.cut_slot(solid)
        solid = self.add_fillet_to_slot_corners(solid)
        solid = self.drill_pin_hole(solid)
        solid = self.add_ribs(solid)
        return solid

result = EjectorSpringRetainer().build()
