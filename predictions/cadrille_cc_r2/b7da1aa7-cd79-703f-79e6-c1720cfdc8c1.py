import cadquery as cq
import math
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_height = 5.0
rib_width = 6.0
rib_thickness = 2.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_distance = 0.5
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
rib = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
rib = rib.translate((0,0, thickness/2))
rib = rib.translate((0,0, thickness/2))
combined = base.union(rib)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (-hole_offset, -hole_offset),
    (hole_offset, -hole_offset),
]
for x, y in hole_positions:
    combined = combined.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
result = combined
