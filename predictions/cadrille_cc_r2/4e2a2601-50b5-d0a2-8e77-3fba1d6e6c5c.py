import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
wall_thickness = 2.0
rib_width = 12.0
rib_height = 8.0
rib_thickness = 4.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 15.0
chamfer_size = 0.5
base = cq.Workplane('XY').rect(leg_length, leg_width).extrude(thickness)
rib = cq.Workplane('XY').rect(leg_width, rib_height).extrude(thickness)
rib = rib.edges().chamfer(chamfer_size)
rib = rib.edges().chamfer(chamfer_size)
rib = rib.translate((leg_length/2 - wall_thickness - rib_thickness/2, 0, 0))
rib = rib.translate((leg_length/2 - wall_thickness - rib_thickness/2, 0, 0))
result = base.union(rib)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, -hole_offset),
    (hole_offset, hole_offset),
]
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
result = result.edges('|Z').chamfer(chamfer_size)
