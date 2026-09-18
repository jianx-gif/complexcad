import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 10.0
chamfer_distance = 2.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_count = 6
hole_radius = outer_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)
base = base.edges().chamfer(chamfer_distance)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
result = base
