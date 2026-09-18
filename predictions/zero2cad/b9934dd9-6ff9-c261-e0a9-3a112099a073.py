import cadquery as cq
import math

outer_radius = 30.0
wall_thickness = 6.0
inner_radius = outer_radius - wall_thickness
height = 50.0
base_thickness = 4.0
base_width = 80.0
base_length = 80.0
chamfer_size = 1.5
hole_diameter = 4.0
hole_depth = 12.0
hole_count = 6
hole_radius = outer_radius - wall_thickness/2

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(inner_radius, height)
    .close()
)

shell = profile.revolve()

base = (
    cq.Workplane("XY")
    .rect(base_width, base_length)
    .extrude(base_thickness)
    .translate((0, 0, -base_thickness))
)

result = shell.union(base)

result = result.edges("|Z").chamfer(chamfer_size)

points = [
    (hole_radius * math.cos(2 * math.pi * i / hole_count),
     hole_radius * math.sin(2 * math.pi * i / hole_count))
    for i in range(hole_count)
]

holes = (
    cq.Workplane("XY")
    .pushPoints(points)
    .circle(hole_diameter / 2)
    .extrude(-hole_depth)
    .translate((0, 0, height))
)

result = result.cut(holes)
