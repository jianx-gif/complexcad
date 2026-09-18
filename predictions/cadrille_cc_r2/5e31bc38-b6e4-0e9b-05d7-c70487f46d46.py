import cadquery as cq
import math
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
chamfer_distance = 2.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 8
hole_radius = hole_diameter / 2.0
hole_offset = 15.0
chamfer_distance = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(thickness)
)
base = base.cut(inner_cyl)
hole_positions = [
    (hole_offset, 0),
    (0, hole_offset),
    (hole_offset, hole_offset),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
base = base.edges("|Z").chamfer(chamfer_distance)
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .circle(hole_radius)
    .cutBlind(-thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .circle(hole_radius)
    .cutBlind(-thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .circle(hole_radius)
    .cutBlind(-chamfer_distance)
)
result = base
