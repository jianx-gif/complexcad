import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_diameter = 30.0,
    inner_diameter = 20.0,
    wall_thickness = 2.0,
    top_fillet_radius = 2.0,
    top_fillet_radius = 0.5,
    top_fillet_radius = 0.5,
    top_fillet_radius = 0.5,
    hole_diameter = 5.0,
    hole_offset = 10.0,
    hole_depth = 8.0,
    hole_count = 4
)
m.outer_radius = 0.5 * m.outer_diameter
m.outer_radius = m.outer_radius - m.wall_thickness
m.outer_height = m.outer_height - m.wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(m.outer_radius, 0)
    .lineTo(m.outer_radius, m.outer_height)
    .lineTo(m.outer_radius + m.wall_thickness, m.outer_height)
    .lineTo(m.outer_radius + m.wall_thickness, m.outer_height + m.wall_thickness)
    .lineTo(m.outer_radius, m.outer_height + m.wall_thickness)
    .lineTo(m.outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(m.chamfer_distance)
solid = solid.faces(">Z").workplane().hole(m.hole_diameter)
solid = solid.faces(">Z").workplane().hole(m.hole_diameter)
solid = solid.faces(">Z").workplane().hole(m.hole_diameter)
solid = solid.faces(">Z").workplane().hole(m.hole_diameter)
solid = solid.faces(">Z").edges().chamfer(m.chamfer_distance)
result = solid
