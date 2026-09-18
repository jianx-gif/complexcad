import cadquery as cq

leg_length = 80.0
leg_width = 20.0
thickness = 10.0
fillet_radius = 0.5
chamfer_distance = 1.0
hole_diameter = 4.0
hole_spacing = 30.0
edge_offset = 10.0
num_holes = int((leg_length - 2 * edge_offset) // hole_spacing) + 1

# Create base L shape
pts = [(0, 0), (leg_length, 0), (leg_length, thickness), (thickness, thickness), (thickness, leg_width), (0, leg_width)]
solid = cq.Workplane('XY').polyline(pts).close().extrude(thickness)
# Add holes
horiz_positions = [(edge_offset + i * hole_spacing, thickness/2) for i in range(num_holes) if edge_offset + i * hole_spacing < leg_length]
solid = solid.faces('>Z').workplane().pushPoints(horiz_positions).hole(hole_diameter)
vert_positions = [(thickness/2, edge_offset + i * hole_spacing) for i in range(num_holes) if edge_offset + i * hole_spacing < leg_width]
solid = solid.faces('>Y').workplane().pushPoints(vert_positions).hole(hole_diameter)
# Chamfer outer edges
solid = solid.edges('not |Z').chamfer(chamfer_distance)
# Fillet interior Z edges
solid = solid.edges('|Z').fillet(fillet_radius)
result = solid
