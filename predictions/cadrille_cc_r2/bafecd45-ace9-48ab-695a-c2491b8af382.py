import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 8.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 15.0
rib_count = 4
rib_count = 2
base = cq.Workplane('XY').rect(leg_length, leg_width).extrude(thickness)
rib = cq.Workplane('XY').rect(leg_width, rib_height).extrude(thickness)
rib = rib.translate((leg_length/2 - rib_thickness/2, leg_width/2, 0))
result = base.union(rib)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, -hole_offset),
    (hole_offset, -hole_offset),
]
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
result = result.faces('>Z').workplane().center(hole_offset, hole_offset).hole(hole_diameter)
result = result.faces('>Z').workplane().center(hole_offset, hole_offset).hole(hole_diameter)
result = result.faces('>Z').workplane().center(hole_offset, hole_offset).hole(hole_diameter)
result = result.faces('>Z').workplane().center(hole_offset, hole_offset).hole(hole_diameter)
