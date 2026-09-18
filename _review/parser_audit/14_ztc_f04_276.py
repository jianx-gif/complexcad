import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    outer_diameter = 80.0,
    block_thickness = 12.0,
    block_height = 15.0,
    fillet_radius = 2.0,
    top_fillet_radius = 1.5,
    chamfer_distance = 0.8,
    hole_diameter = 4.0,
    hole_spacing_angle = 20.0,
    hole_pattern_radius = 6.0
)

m.outer_radius = 0.5 * m.outer_diameter
m.sweep_radius = m.outer_radius - 0.5 * m.block_thickness
m.linear_width = 2.0 * m.sweep_radius
m.hole_count = int(180.0 / m.hole_spacing_angle) + 1

path = (
    cq.Workplane('XY')
    .radiusArc((m.linear_width, 0.0), m.sweep_radius)
    .wire()
)

result = (
    cq.Workplane('XY')
    .transformed(rotate=(90, 0, 0))
    .rect(m.block_thickness, m.block_height)
    .sweep(path, transition='round')
    .edges('|Z')
    .fillet(m.fillet_radius)
    .edges('>Z')
    .fillet(m.top_fillet_radius)
    .edges('<Z')
    .chamfer(m.chamfer_distance)
    .faces('>Z')
    .workplane()
    .polarArray(count=m.hole_count, startAngle=-90, angle=180, radius=m.hole_pattern_radius)
    .hole(m.hole_diameter)
)
