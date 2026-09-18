import cadquery as cq
import math
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
chamfer_distance = 2.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset = 15.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
rib_count = 4
rib_count = 4
rib_offset = 10.0
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
rib = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
rib = rib.translate((0, 0, thickness/2))
rib = rib.translate((0, 0, thickness/2))
rib = rib.translate((0, 0, thickness/2))
combined = base.union(rib)
combined = combined.edges('|Z').chamfer(chamfer_distance)
hole_positions = [
    ( hole_offset,  hole_offset),
    (-hole_offset,  hole_offset),
    ( hole_offset, -hole_offset),
    (-hole_offset, -hole_offset),
]
combined = combined.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
combined = combined.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
combined = combined.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_width)
combined = combined.edges('|Z').chamfer(chamfer_distance)
result = combined
