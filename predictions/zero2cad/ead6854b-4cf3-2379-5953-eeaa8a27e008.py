import cadquery as cq
import math
triangle_side = 80.0
thickness = 10.0
hole_diameter = 20.0
chamfer_distance = 2.0
tab_width = 15.0
tab_length = 25.0
tab_thickness = thickness
triangle_radius = triangle_side / math.sqrt(3)
base = (
    cq.Workplane("XY")
    .polygon(3, triangle_radius)
    .extrude(thickness)
)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.edges("|Z").chamfer(chamfer_distance)
# create tab on +X side
tab = (
    base.faces(">X").workplane()
    .rect(tab_width, tab_length)
    .extrude(tab_thickness)
)
result = base.union(tab)
