import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    base_width=60.0,
    base_depth=30.0,
    base_thickness=5.0,
    boss_width=20.0,
    boss_depth=20.0,
    boss_height=8.0,
    hole_diameter=4.0,
    hole_depth=6.0,
    hole_spacing=12.0,
    chamfer=0.8,
    rib_thickness=2.0,
    rib_height=3.0,
    rib_spacing=10.0
)

# Base plate
base = (
    cq.Workplane("XY")
    .rect(m.base_width, m.base_depth)
    .extrude(m.base_thickness)
)

# Central boss
boss = (
    base.faces(">Z").workplane()
    .rect(m.boss_width, m.boss_depth)
    .extrude(m.boss_height)
)

# Blind holes in boss
hole_positions = [
    (-m.hole_spacing/2, 0),
    (m.hole_spacing/2, 0)
]

boss_with_holes = (
    boss.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(m.hole_diameter, depth=m.hole_depth)
)

# Ribs on underside of base
rib_count = int((m.base_width - 2*m.rib_spacing) // m.rib_spacing) + 1
rib_positions = [(-m.base_width/2 + m.rib_spacing + i*m.rib_spacing, 0) for i in range(rib_count)]

ribs = (
    base.faces("<Z").workplane()
    .pushPoints(rib_positions)
    .rect(m.rib_thickness, m.base_depth - 2*m.rib_spacing)
    .extrude(-m.rib_height)
)

# Combine all features
combined = base.union(boss_with_holes).union(ribs)

# Chamfer outer edges of base
result = (
    combined.edges("<<Z")
    .chamfer(m.chamfer)
)
