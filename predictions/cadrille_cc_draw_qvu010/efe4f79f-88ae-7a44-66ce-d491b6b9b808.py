import cadquery as cq
import math
base_length = 100.0
base_width = 30.0
base_thickness = 10.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_count = 6
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
base = base.edges("|Z").chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, base_width)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
base = base.union(rib)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
base = base.faces(">Z").edges().chamfer(chamfer_size)
result = base
