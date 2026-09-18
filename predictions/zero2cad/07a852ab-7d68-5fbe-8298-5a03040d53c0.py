import cadquery as cq
import math

outer_radius = 45.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
height = 20.0
lip_height = 4.0
lip_thickness = 3.0
split_gap = 2.0
hole_diameter = 5.0
hole_count = 4
hole_radius = outer_radius - wall_thickness/2

profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(outer_radius - lip_thickness, height)
    .lineTo(outer_radius - lip_thickness, height + lip_height)
    .lineTo(inner_radius, height + lip_height)
    .lineTo(inner_radius, 0)
    .close()
)

solid = profile.revolve()

split_cut = (
    cq.Workplane("XY")
    .box(split_gap, outer_radius * 2, height + lip_height)
    .translate((0, 0, (height + lip_height) / 2))
)

solid = solid.cut(split_cut)

hole_positions = [
    (hole_radius * math.cos(2 * math.pi * i / hole_count),
     hole_radius * math.sin(2 * math.pi * i / hole_count))
    for i in range(hole_count)
]

solid = (
    solid.workplane(offset=height + lip_height)
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

result = solid
