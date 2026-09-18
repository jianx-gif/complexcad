import cadquery as cq
import math
radius = 30
thickness = 10
height = 5
chamfer = 1
hole_diameter = 5
hole_spacing = 45
hole_depth = 8
hole_count = 6
hole_pattern = 2
hole_pattern = 2
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(radius, 0)
    .lineTo(radius, height)
    .lineTo(radius, height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=hole_pattern, count=hole_count, startAngle=0, angle=360).hole(hole_diameter)
solid = solid.edges().chamfer(chamfer)
result = solid
