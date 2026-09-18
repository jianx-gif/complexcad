import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 15.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 6
base = cq.Workplane('XY').rect(leg_length, leg_width).extrude(thickness)
base = base.edges('|Z').chamfer(chamfer_size)
hole_positions = [
    (hole_offset, leg_width/2 - hole_offset),
    (-hole_offset, leg_width/2 - hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, -hole_offset),
]
base = base.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
rib = cq.Workplane('XY').rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.translate((leg_length/2 - rib_thickness/2, leg_width/2, 0))
result = base.union(rib)
result = result.faces('>Z').workplane().pushPoints(rib_positions).hole(hole_diameter)
result = result.edges('|Z').chamfer(chamfer_size)
