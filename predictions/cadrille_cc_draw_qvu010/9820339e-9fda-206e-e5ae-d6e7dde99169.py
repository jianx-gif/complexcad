import cadquery as cq
import math
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 20.0
rib_width = 5.0
rib_height = 12.0
rib_thickness = 4.0
rib_spacing = 12.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_depth = 8.0
hole_count = 6
hole_radius = outer_diameter / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2.0, 0)
    .lineTo(inner_diameter / 2.0, thickness)
    .lineTo(outer_diameter / 2.0, thickness)
    .lineTo(outer_diameter / 2.0, 0)
    .close()
)
solid = profile.revolve()
solid = solid.shell(-thickness)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
hole_positions = [
    (hole_radius * math.cos(2 * math.pi * i / hole_count),
     hole_radius * math.sin(2 * math.pi * i / hole_count))
    for i in range(hole_count)
]
solid = (
    solid.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
solid = solid.edges("|Z").chamfer(chamfer_size)
result = solid
