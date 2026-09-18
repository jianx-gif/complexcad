import cadquery as cq
import math
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
chamfer_distance = 2.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset = 15.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 15.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
base = base.edges().chamfer(chamfer_distance)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_thickness)
base = base.faces(">Z").workplane().rect(rib_width, rib_height).cutBlind(-rib_thickness)
base = base.faces(">Z").workplane().rect(rib_width, rib_height).cutBlind(-rib_thickness)
base = base.faces(">Z").workplane().rect(rib_width, rib_height).cutBlind(-rib_thickness)
base = base.faces(">Z").workplane().rect(rib_width, rib_height).cutBlind(-rib_thickness)
base = base.faces(">Z").workplane().rect(rib_width, rib_height).cutBlind(-rib_thickness)
result = base
