import cadquery as cq
from types import SimpleNamespace as Measures

# Parameter definitions
m = Measures(
    width=80.0,
    height=60.0,
    base_thickness=4.0,
    boss_diameter=25.0,
    boss_height=6.0,
    hole_diameter=8.0,
    countersink_diameter=12.0,
    hole_margin=12.0,
    chamfer=1.5,
)

# Base plate
base = (
    cq.Workplane("XY")
    .rect(m.width, m.height)
    .extrude(m.base_thickness)
)

# Central boss atop base
boss = (
    cq.Workplane("XY")
    .circle(m.boss_diameter / 2)
    .extrude(m.boss_height)
    .translate((0, 0, m.base_thickness))
)

# Combine base and boss
combined = base.union(boss)

# Offsets for peripheral holes
offset_x = m.width / 2 - m.hole_margin
offset_y = m.height / 2 - m.hole_margin
hole_positions = [
    ( offset_x,  offset_y),
    ( offset_x, -offset_y),
    (-offset_x,  offset_y),
    (-offset_x, -offset_y),
]

# Add countersunk holes on top surface of base (through boss as well)
spaced = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cboreHole(
        m.hole_diameter,
        m.base_thickness + m.boss_height,
        m.countersink_diameter,
    )
)

# Apply beveled edge (chamfer) around outer perimeter
result = (
    spaced
    .edges("|X or |Y")
    .chamfer(m.chamfer)
)
