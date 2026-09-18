import cadquery as cq
import math
outer_diameter = 70.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = inner_diameter / 2.0
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .rect(outer_diameter, outer_diameter)
    .extrude(outer_diameter)
)
base = base.edges().chamfer(chamfer_size)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (0, hole_offset + hole_spacing),
    (hole_offset, hole_offset + hole_spacing)
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
    .rect(inner_radius * 2, inner_radius * 2)
    .cutBlind(-inner_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(inner_radius * 2, inner_radius * 2)
    .cutBlind(-inner_diameter)
)
result = base
