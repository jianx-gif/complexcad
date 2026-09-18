import cadquery as cq
import math
outer_diameter = 30.0
wall_thickness = 3.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_offset = wall_thickness + 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(base)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(base)
)
base = base.cut(inner_cyl)
base = base.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (inner_radius + wall_thickness + hole_offset, 0)
    for i in range(hole_count)
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(inner_diameter, inner_diameter)
    .cutBlind(-wall_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(inner_diameter, inner_diameter)
    .cutBlind(-wall_thickness)
)
base = base.edges("|Z").chamfer(chamfer_size)
result = base
