import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    plate_width=80.0,
    plate_depth=50.0,
    plate_thickness=5.0,
    fillet_radius=2.0,
    chamfer_distance=0.5,
    oval_width=40.0,
    oval_height=20.0,
    boss_diameter=6.0,
    boss_height=4.0,
    boss_spacing=20.0,
    boss_count=3,
    hole_diameter=2.5,
    cbore_diameter=5.0,
    cbore_depth=2.0,
    hole_spacing=20.0,
    hole_count=3
)

# Base plate
result = (
    cq.Workplane("XY")
    .box(m.plate_width, m.plate_depth, m.plate_thickness)
    .translate((0.5 * m.plate_width, 0, 0.5 * m.plate_thickness))
    .faces(">Z").edges().fillet(m.fillet_radius)
    .faces("<Z").edges().chamfer(m.chamfer_distance)
)

# Central oval cutout through the plate
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .ellipse(m.oval_width / 2, m.oval_height / 2)
    .cutBlind(-m.plate_thickness)
)

# Add cylindrical bosses on top surface
boss_positions = []
start_x = (m.plate_width - (m.boss_count - 1) * m.boss_spacing) / 2
for i in range(m.boss_count):
    boss_positions.append((start_x + i * m.boss_spacing, -m.plate_depth / 2 + m.boss_diameter / 2))

result = (
    result.faces(">Z").workplane()
    .pushPoints(boss_positions)
    .circle(m.boss_diameter / 2)
    .extrude(m.boss_height)
)

# Add counterbore holes aligned with bosses
hole_positions = []
for i in range(m.boss_count):
    hole_positions.append((start_x + i * m.boss_spacing, -m.plate_depth / 2 + m.boss_diameter / 2))

result = (
    result.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .cboreHole(m.hole_diameter, m.cbore_diameter, m.cbore_depth)
)
