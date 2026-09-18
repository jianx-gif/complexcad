import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_diameter = 40.0,
    inner_diameter = 30.0,
    outer_height = 12.0,
    rib_height = 8.0,
    rib_width = 6.0,
    rib_depth = 4.0,
    rib_count = 4,
    rib_offset = 10.0,
    rib_chamfer = 1.0
)
m = measures
base = (
    cq.Workplane("XY")
    .rect(m.outer_diameter, m.outer_diameter)
    .extrude(m.outer_height)
)
rib = (
    cq.Workplane("XY")
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_depth)
    .translate((0, 0, m.rib_height))
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(m.chamfer)
combined = combined.faces(">Z").workplane().hole(m.rib_chamfer)
combined = combined.faces(">Z").edges().chamfer(m.rib_chamfer)
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-m.outer_diameter/2 + m.rib_offset, 0),
        ( m.outer_diameter/2 - m.rib_offset, 0),
        (-m.outer_diameter/2 + m.rib_offset, -m.outer_height/2 + m.rib_height),
        ( m.outer_diameter/2 - m.rib_offset, -m.outer_height/2 + m.rib_height),
        (-m.outer_diameter/2 + m.rib_offset, -m.outer_height/2 + m.rib_height),
        ( m.outer_diameter/2 - m.rib_offset, -m.outer_height/2 + m.rib_height),
        (-m.outer_diameter/2 + m.rib_offset, -m.outer_height/2 + m.rib_height),
        ( m.outer_diameter/2 - m.rib_offset, -m.outer_height/2 + m.rib_height),
        (-m.outer_diameter/2 + m.rib_offset, -m.outer_height/2 + m.rib_height),
        ( m.outer_diameter/2 - m.rib_offset, -m.outer_height/2 + m.rib_height)
    ])
    .close()
    .extrude(m.rib_depth)
)
