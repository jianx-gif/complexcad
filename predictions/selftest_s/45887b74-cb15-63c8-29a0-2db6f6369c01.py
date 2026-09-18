
import cadquery as cq

class Measures:
    def __init__(self, horizontal_leg, vertical_leg, thickness, width, fillet_radius, counterbore_dia, counterbore_depth, clearance_dia, hole_spacing, hole_dia, gusset_thickness):
        self.horizontal_leg = horizontal_leg
        self.vertical_leg = vertical_leg
        self.thickness = thickness
        self.width = width
        self.fillet_radius = fillet_radius
        self.counterbore_dia = counterbore_dia
        self.counterbore_depth = counterbore_depth
        self.clearance_dia = clearance_dia
        self.hole_spacing = hole_spacing
        self.hole_dia = hole_dia
        self.gusset_thickness = gusset_thickness

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()
    def build(self):
        m = self.measures
        # L profile
        profile = (
            cq.Workplane('XY')
            .lineTo(m.horizontal_leg, 0)
            .lineTo(m.horizontal_leg, m.thickness)
            .lineTo(m.thickness, m.thickness)
            .lineTo(m.thickness, m.vertical_leg)
            .close()
        )
        self.model = profile.extrude(m.width)
        # Counterbore on vertical side
        self.model = (
            self.model
            .faces('<X')
            .workplane(centerOption='CenterOfBoundBox')
            .move(0, m.vertical_leg/2)
            .cboreHole(m.clearance_dia, m.counterbore_dia, m.counterbore_depth)
        )
        # Clearance holes on horizontal leg
        self.model = (
            self.model
            .faces('>Y')
            .workplane(centerOption='CenterOfBoundBox')
            .rarray(m.hole_spacing, 0, int(m.horizontal_leg/m.hole_spacing), 1)
            .hole(m.hole_dia)
        )
        # Fillet inner bend
        self.model = (
            self.model
            .edges()
            .filter(lambda e: abs(e.Center().x - m.thickness) < 0.001 and abs(e.Center().y - m.thickness) < 0.001)
            .fillet(m.fillet_radius)
        )
        # Triangular gusset in inner corner for reinforcement
        gusset = (
            cq.Workplane('XY')
            .moveTo(m.thickness/2, m.thickness/2)
            .lineTo(m.thickness, m.thickness/2)
            .lineTo(m.thickness/2, m.thickness)
            .close()
            .extrude(m.gusset_thickness)
        )
        self.model = self.model.union(gusset)

# Define parameters within 100-unit max
meas = Measures(
    horizontal_leg=80.0,
    vertical_leg=60.0,
    thickness=10.0,
    width=12.0,
    fillet_radius=2.0,
    counterbore_dia=8.0,
    counterbore_depth=3.0,
    clearance_dia=6.0,
    hole_spacing=20.0,
    hole_dia=4.0,
    gusset_thickness=5.0
)

result = LBracket(cq.Workplane('XY'), meas).model
