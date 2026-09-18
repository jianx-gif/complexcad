import cadquery as cq
from types import SimpleNamespace as Measures

horizontal_leg_length = 70.0
vertical_leg_length = 80.0
leg_thickness = 12.0
base_thickness = 15.0
relief_cut_width = 20.0
relief_cut_depth = 5.0
relief_cut_offset_x = leg_thickness / 2
relief_cut_offset_y = leg_thickness + 30.0
hole_diameter = 6.0
hole_clearance = 6.5
hole_spacing = 40.0
hole_offset_y = leg_thickness / 2
gusset_thickness = 10.0
chamfer_size = 1.0

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()
    def build(self):
        m = self.measures
        # L profile sketch
        pts = [
            (0, 0),
            (m.horizontal_leg_length, 0),
            (m.horizontal_leg_length, m.leg_thickness),
            (m.leg_thickness, m.leg_thickness),
            (m.leg_thickness, m.vertical_leg_length + m.leg_thickness),
            (0, m.vertical_leg_length + m.leg_thickness),
            (0, 0)
        ]
        self.model = (
            cq.Workplane("XY")
            .polyline(pts)
            .close()
            .extrude(m.base_thickness)
        )
        # Relief cut on vertical leg
        self.model = (
            self.model.faces(">Z")
            .workplane()
            .center(m.relief_cut_offset_x, m.relief_cut_offset_y)
            .rect(m.relief_cut_width, m.relief_cut_depth)
            .cutBlind(-m.relief_cut_depth)
        )
        # Clearance holes on horizontal leg
        self.model = (
            self.model.faces(">Z")
            .workplane()
            .center(m.horizontal_leg_length/2, m.hole_offset_y)
            .pushPoints([(-m.hole_spacing/2, 0), (m.hole_spacing/2, 0)])
            .hole(m.hole_clearance)
        )
        # Gusset triangular brace
        gusset_pts = [
            (0, 0),
            (m.gusset_thickness, 0),
            (0, m.gusset_thickness)
        ]
        self.model = (
            self.model.faces("<Y")
            .workplane(origin=(0,0,0), offset=-m.base_thickness/2)
            .move(m.leg_thickness/2, m.leg_thickness/2)
            .polyline(gusset_pts)
            .close()
            .extrude(m.base_thickness)
        )
        # Chamfer outer edges
        self.model = self.model.edges("|Z").chamfer(m.chamfer_size)

measures = Measures(
    horizontal_leg_length=horizontal_leg_length,
    vertical_leg_length=vertical_leg_length,
    leg_thickness=leg_thickness,
    base_thickness=base_thickness,
    relief_cut_width=relief_cut_width,
    relief_cut_depth=relief_cut_depth,
    relief_cut_offset_x=relief_cut_offset_x,
    relief_cut_offset_y=relief_cut_offset_y,
    hole_diameter=hole_diameter,
    hole_clearance=hole_clearance,
    hole_spacing=hole_spacing,
    hole_offset_y=hole_offset_y,
    gusset_thickness=gusset_thickness,
    chamfer_size=chamfer_size,
)

result = LBracket(cq.Workplane("XY"), measures).model
