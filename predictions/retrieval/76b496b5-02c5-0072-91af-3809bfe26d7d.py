import cadquery as cq
from types import SimpleNamespace as Measures

# Parameters (max dimension 100)
width_long_leg = 80.0
width_short_leg = 60.0
material_thickness = 10.0
chamfer_size = 2.0
hole_clearance = 5.0
counterbore_dia = 8.0
counterbore_depth = 4.0
hole_spacing = 20.0
hole_count_along_long = 3
hole_offset_from_edge = 12.0
slot_width = 15.0
slot_depth = 5.0  # pocket depth, half of material thickness

measures = Measures(
    width_long_leg=width_long_leg,
    width_short_leg=width_short_leg,
    material_thickness=material_thickness,
    chamfer_size=chamfer_size,
    hole_clearance=hole_clearance,
    counterbore_dia=counterbore_dia,
    counterbore_depth=counterbore_depth,
    hole_spacing=hole_spacing,
    hole_count_along_long=hole_count_along_long,
    hole_offset_from_edge=hole_offset_from_edge,
    slot_width=slot_width,
    slot_depth=slot_depth,
)

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        profile = (
            cq.Workplane("XY")
            .polyline([
                (0, 0),
                (m.width_short_leg, 0),
                (m.width_short_leg, m.material_thickness),
                (m.material_thickness, m.material_thickness),
                (m.material_thickness, m.width_long_leg),
                (0, m.width_long_leg),
                (0, 0),
            ])
            .close()
        )
        self.model = profile.extrude(m.material_thickness)
        # Pocket cutout on short leg (does not cut fully through)
        self.model = (
            self.model.faces(">Z")
            .workplane()
            .center(m.width_short_leg/2, m.material_thickness/2)
            .rect(m.slot_width, m.slot_depth)
            .cutBlind(-m.slot_depth)
        )
        # Chamfer outer vertical edges on +X face
        self.model = self.model.faces(">X").edges().chamfer(m.chamfer_size)
        # Chamfer outer vertical edges on +Y face
        self.model = self.model.faces(">Y").edges().chamfer(m.chamfer_size)
        # Counterbore hole array on long leg face
        self.model = (
            self.model.faces(">Z")
            .workplane()
            .center(m.material_thickness/2 + m.hole_offset_from_edge, m.material_thickness/2 + m.hole_offset_from_edge)
            .rarray(m.hole_spacing, 0, m.hole_count_along_long, 1)
            .cboreHole(m.hole_clearance, m.counterbore_dia, m.counterbore_depth)
        )

result = LBracket(cq.Workplane("XY"), measures).model
