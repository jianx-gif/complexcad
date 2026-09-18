import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 20.0
thickness = 20.0
rib_width = 12.0
rib_height = 10.0
rib_thickness = 4.0
rib_spacing = 12.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_depth = thickness / 2.0
hole_count = 12
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2.0, 0)
    .lineTo(inner_diameter / 2.0, thickness / 2.0)
    .lineTo(inner_diameter / 2.0, thickness / 2.0)
    .lineTo(inner_diameter / 2.0, 0)
    .close()
)
solid = profile.revolve()
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(inner_diameter / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
solid = solid.union(rib)
hole_positions = [
    (inner_diameter / 2.0 + hole_depth / 2.0, hole_depth / 2.0 + hole_spacing / 2.0)
]
solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
solid = solid.edges().chamfer(chamfer_size)
result = solid
