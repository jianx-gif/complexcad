import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_diameter = 60.0,
    inner_diameter = 30.0,
    thickness = 10.0,
    outer_fillet = 2.0,
    top_fillet = 0.5,
    top_fillet = 0.5,
    hole_diameter = 8.0,
    hole_depth = 2.0,
    hole_offset_x = 15.0,
    hole_offset_y = 10.0
)
m.outer_radius = 0.5 * m.outer_diameter
m.outer_fillet = m.outer_radius - m.outer_radius
m.outer_fillet = m.outer_fillet
m.outer_fillet = m.outer_radius - m.outer_radius
m.outer_fillet = m.outer_fillet
m.outer_fillet = m.outer_fillet
m.outer_fillet = m.outer_fillet
m.outer_fillet = m.outer_fillet
m.outer_fillet = m.outer_fillet
m.outer_fillet = m.outer_fillet
m.outer_fillet = m.outer_fillet
m.outer_fillet = m.outer_fillet
m.outer_fillet = m.outer_fillet
m.outer_fillet = m.outer_fillet.mirror(m.inner_fillet)
m.outer_fillet = m.outer_fillet.mirror(mirrorPlane="YZ")
m.outer_fillet = m.outer_fillet.mirror(mirrorPlane="YZ").circle(m.outer_fillet).extrude(m.thickness)
m.outer_fillet = m.outer_fillet.mirror(mirrorPlane="YZ").circle(m.inner_fillet).extrude(m.thickness)
result = m.outer_fillet.union(m.outer_fillet)
