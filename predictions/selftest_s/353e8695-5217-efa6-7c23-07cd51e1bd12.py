import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    outer_radius=30.0,
    wall_thickness=5.0,
    height=40.0,
    rib_count=8,
    rib_width=3.0,
    rib_thickness=1.0,
    rib_height=30.0,
    chamfer_size=1.0,
    lid_groove_radius=25.0,
    lid_groove_depth=2.0,
)

# Base solids
outer = cq.Workplane("XY").circle(m.outer_radius).extrude(m.height).val()
inner = cq.Workplane("XY").circle(m.outer_radius - m.wall_thickness).extrude(m.height).val()

shell = outer.cut(inner)

# Generate ribs around interior
rib_entities = []
for i in range(m.rib_count):
    angle = i * 360.0 / m.rib_count
    rib = (
        cq.Workplane("XY")
        .box(m.rib_width, m.rib_thickness, m.rib_height)
        .translate((m.outer_radius - m.wall_thickness - m.rib_width / 2, 0, m.rib_height / 2))
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    rib_entities.append(rib)

ribs_combined = cq.Workplane("XY")
for rib in rib_entities:
    ribs_combined = ribs_combined.union(rib)

# Combine ribs with shell
combined = cq.Workplane(combined:=shell).union(ribs_combined)

# Chamfer top rim
chamfered = combined.faces(">Z").edges().chamfer(m.chamfer_size)

# Press‑fit lid groove below top surface
result = (
    chamfered
    .faces(">Z")
    .workplane(offset=-m.lid_groove_depth / 2)
    .circle(m.lid_groove_radius)
    .cutBlind(-m.lid_groove_depth)
)
