import cadquery as cq
import math
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
chamfer_distance = 2.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_count = 8
hole_radius = hole_diameter / 2.0
hole_offset = 15.0
chamfer_distance = 0.5
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)
base = base.edges("|Z").chamfer(chamfer_distance)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().rect(hole_diameter, hole_diameter).cutBlind(-thickness)
base = base.faces(">Z").workplane().rect(hole_diameter, hole_diameter).cutBlind(-thickness)
base = base.faces(">Z").workplane().rect(hole_diameter, hole_diameter).cutBlind(-thickness)
base = base.faces(">Z").workplane().rect(hole_diameter, hole_diameter).cutBlind(-thickness)
base = base.faces(">Z").workplane().rect(hole_diameter, hole_diameter).cutBlind(-thickness)
base = base.faces(">Z").workplane().rect(hole_diameter, hole_diameter).cutBlind(-thickness)
base = base.faces(">Z").workplane().rect(hole_diameter, hole_diameter).cutBlind(-thickness)
base = base.faces(">Z").workplane().rect(hole_diameter, hole_diameter).cutBlind(-thickness)
base = base.faces(">Z").workplane().rect(hole_diameter, hole_diameter).cutBlind(-thickness)
base = base.faces(">Z").workplane().rect(hole_diameter, hole_diameter).cutBlind(-thickness)
result = base
