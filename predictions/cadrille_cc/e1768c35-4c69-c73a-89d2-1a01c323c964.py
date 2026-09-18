import cadquery as cq
import math
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
height = 12.0
fillet_radius = 2.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 6
hole_offset = height / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(outer_radius, height)
    .lineTo(inner_radius, height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(fillet_radius)
solid = solid.edges().fillet(fillet_radius)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces("<Z").workplane().hole(hole_diameter, depth=hole_offset)
solid = solid.faces("<Z").workplane().hole(hole_diameter, depth=hole_offset)
result = solid
