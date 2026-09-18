import cadquery as cq
import math
height = 60.0
inner_radius = 20.0
outer_radius = 30.0
top_chamfer = 2.0
taper_height = 15.0
taper_inner_radius = inner_radius + 2.0
taper_inner_radius = outer_radius - taper_height
side_hole_diameter = 8.0
side_hole_depth = 10.0
side_hole_count = 6
side_hole_spacing = 6.0
hole_radius = (outer_radius + outer_radius) / 2.0
hole_count = 6
hole_depth = height / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height)
    .lineTo(outer_radius, height)
    .lineTo(outer_radius, height + side_hole_depth)
    .lineTo(outer_radius, height + side_hole_depth)
    .lineTo(outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.faces(">Z").edges().chamfer(top_chamfer)
hole_cylinder = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(hole_radius)
    .extrude(height)
    .translate((0, 0, height))
)
solid = solid.cut(hole_cylinder)
result = solid
