import cadquery as cq
import math
base_radius = 20.0
base_height = 15.0
wall_thickness = 2.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 4
hole_radius = base_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(base_height)
)
rib = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(rib_height)
    .translate((0, 0, base_height))
)
base = base.union(rib)
rib = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(rib_height)
    .translate((0, 0, base_height))
)
base = base.union(rib)
hole_positions = [
    (hole_count - 1) * hole_spacing, 0)
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
    .center(hole_positions, 0)
    .hole(hole_diameter)
)
base = base.edges("|Z").chamfer(chamfer_distance)
result = base
