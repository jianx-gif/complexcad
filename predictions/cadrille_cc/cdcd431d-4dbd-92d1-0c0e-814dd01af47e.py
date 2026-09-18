import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 12.0
fillet_radius = 2.0
chamfer_distance = 0.5
hole_diameter = 5.0
hole_spacing = 12.0
hole_count = 6
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
base = base.edges("|Z").fillet(fillet_radius)
base = base.edges("<<Z").chamfer(chamfer_distance)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces("<Z").workplane().hole(hole_diameter)
base = base.faces("<Z").workplane().hole(hole_diameter)
base = base.faces("<Z").workplane().hole(hole_diameter)
base = base.faces("<Z").workplane().center(0, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").workplane().center(hole_offset, hole_offset).hole(hole_diameter)
base = base.faces("<Z").edges().fillet(fillet_radius)
result = base
