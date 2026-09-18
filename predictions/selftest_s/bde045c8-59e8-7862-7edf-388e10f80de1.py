import cadquery as cq
from types import SimpleNamespace as Measures

# Parameter definitions (max dimension 100 units)
bracket_width = 80.0
bracket_height = 100.0
bracket_thickness = 10.0
pocket_width = 50.0
pocket_height = 60.0
pocket_depth = 6.0
clearance_hole_dia = 8.0
hole_offset_y = 30.0
hole_spacing = hole_offset_y * 2
chamfer_size = 1.0
rib_width = 8.0
rib_height = 20.0
rib_offset_x = -bracket_width/2 + rib_width/2 + 5.0

# Helper plugin for part creation
def part(self, part_class, measures):
    part_instance = part_class(self, measures)
    return self.newObject(part_instance.model.objects)

cq.Workplane.part = part

class WallMountBracket:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = measures
        self.build()
    def build(self):
        m = self.measures
        # Base plate
        base = (
            cq.Workplane("XY")
            .rect(m.bracket_width, m.bracket_height)
            .extrude(m.bracket_thickness)
        )
        # Recessed pocket on front (+Z) face
        base = (
            base.faces(">Z")
            .workplane()
            .rect(m.pocket_width, m.pocket_height)
            .cutBlind(-m.pocket_depth)
        )
        # Two clearance holes on front face, symmetrically placed
        base = (
            base.faces(">Z")
            .workplane()
            .pushPoints([(-m.hole_spacing/2, 0), (m.hole_spacing/2, 0)])
            .hole(m.clearance_hole_dia)
        )
        # Reinforcing rib on back (-Z) face
        rib = (
            base.faces("<Z")
            .workplane()
            .rect(m.rib_width, m.rib_height)
            .extrude(m.bracket_thickness)
            .translate((m.rib_offset_x, 0, 0))
        )
        # Combine rib with base
        model = base.union(rib)
        # Chamfer outer edges for safety
        model = model.edges("|Z").chamfer(m.chamfer_size)
        self.model = model

measures = Measures(
    bracket_width = bracket_width,
    bracket_height = bracket_height,
    bracket_thickness = bracket_thickness,
    pocket_width = pocket_width,
    pocket_height = pocket_height,
    pocket_depth = pocket_depth,
    clearance_hole_dia = clearance_hole_dia,
    hole_spacing = hole_spacing,
    chamfer_size = chamfer_size,
    rib_width = rib_width,
    rib_height = rib_height,
    rib_offset_x = rib_offset_x,
)

result = WallMountBracket(cq.Workplane("XY"), measures).model