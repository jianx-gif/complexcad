import cadquery as cq
import math
centerline_radius = 30.0
pipe_outer_diameter = 20.0
pipe_wall_thickness = 2.0
insert_diameter = 6.0
insert_length = 12.0
fillet_radius = 2.0
profile = (
    cq.Workplane("XY")
    .moveTo(centerline_radius, 0)
    .radiusArc((centerline_radius, 0), centerline_radius)
    .lineTo(centerline_radius, centerline_radius)
    .radiusArc((centerline_radius, centerline_radius), centerline_radius)
    .lineTo(centerline_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(fillet_radius)
solid = solid.faces(">Z").workplane().hole(insert_diameter)
solid = solid.faces(">Z").workplane().circle(insert_diameter/2).extrude(insert_length)
solid = solid.faces(">Z").workplane().polarArray(radius=hole_radius, count=insert_diameter/2, startAngle=0, angle=360).hole(insert_diameter)
solid = solid.faces(">Z").workplane().center(centerline_radius - pipe_outer_diameter/2, 0).circle(insert_diameter/2).extrude(insert_length)
solid = solid.cut(central)
solid = solid.faces(">Z").workplane().center(centerline_radius - pipe_outer_diameter/2, 0).circle(insert_diameter/2).extrude(insert_length)
solid = solid.faces(">Z").workplane().center(centerline_radius - pipe_outer_diameter/2, 0).circle(insert_diameter/2).extrude(insert_length)
result = solid
