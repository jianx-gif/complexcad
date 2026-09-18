import cadquery as cq
from types import SimpleNamespace as Measures

# Parameters
thickness = 10.0
short_len = 40.0
long_len = 80.0
inner_fillet_radius = 2.0
lattice_spacing = 15.0
lattice_dia = 4.0
m8_hole_dia = 8.6
m8_hole_offset_short = 20.0
m8_hole_offset_long = 10.0

class LBracket:
    def __init__(self, workplane, measures):
        self.model = workplane
        self.measures = measures
        self.build()
    def build(self):
        m = self.measures
        short = (
            cq.Workplane("XY")
            .box(m.short_len, m.thickness, m.thickness)
            .translate((m.short_len/2, m.thickness/2, 0))
        )
        long = (
            cq.Workplane("XY")
            .box(m.thickness, m.long_len, m.thickness)
            .translate((m.thickness/2, m.long_len/2, 0))
        )
        bracket = short.union(long)
        try:
            bracket = bracket.edges("<<X and <<Y and |Z").fillet(m.inner_fillet_radius)
        except Exception:
            pass
        # Internal lattice of cylindrical holes
        cols = int((m.short_len - 2*m.thickness) // m.lattice_spacing)
        rows = int((m.long_len - 2*m.thickness) // m.lattice_spacing)
        bracket = (
            bracket.faces(">Z").workplane()
            .moveTo(m.thickness + m.lattice_spacing/2, m.thickness + m.lattice_spacing/2)
            .rarray(m.lattice_spacing, m.lattice_spacing, cols, rows)
            .hole(m.lattice_dia)
        )
        # M8 clearance hole in short arm
        bracket = (
            bracket.faces(">Z").workplane()
            .move(m.m8_hole_offset_short, m.m8_hole_offset_long)
            .hole(m.m8_hole_dia)
        )
        self.model = bracket

measures = Measures(
    thickness=thickness,
    short_len=short_len,
    long_len=long_len,
    inner_fillet_radius=inner_fillet_radius,
    lattice_spacing=lattice_spacing,
    lattice_dia=lattice_dia,
    m8_hole_dia=m8_hole_dia,
    m8_hole_offset_short=m8_hole_offset_short,
    m8_hole_offset_long=m8_hole_offset_long,
)

result = LBracket(cq.Workplane("XY"), measures).model
