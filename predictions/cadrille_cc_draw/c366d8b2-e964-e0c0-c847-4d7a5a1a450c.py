import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_diameter = 30.0,
    inner_diameter = 20.0,
    wall_thickness = 5.0,
    rib_width = 12.0,
    rib_height = 8.0,
    rib_thickness = 4.0,
    rib_count = 6,
    rib_spacing = 15.0,
    rib_offset = 10.0,
    chamfer_distance = 0.5,
    hole_diameter = 5.0,
    hole_spacing = 12.0
)
m.outer_radius = 0.5 * m.outer_diameter
m.outer_radius = m.outer_radius - m.rib_thickness
m.outer = (
    cq.Workplane("XY")
    .radiusArc((m.outer_radius, 0), m.outer_radius)
    .wire()
)
rib = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.outer_radius, 0))
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
)
rib = rib.translate((0, 0, m.rib_height/2))
combined = m.outer.union(rib)
combined = combined.edges("|Z").chamfer(m.chamfer_distance)
combined = combined.faces(">Z").workplane().hole(m.hole_diameter)
combined = combined.faces(">Z").workplane().hole(m.hole_diameter)
result = combined
