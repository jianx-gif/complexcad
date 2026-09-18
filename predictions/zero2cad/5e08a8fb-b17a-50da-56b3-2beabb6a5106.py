import cadquery as cq

block_length = 80.0
block_width = 50.0
block_height = 30.0
wall_thickness = 4.0
rib_thickness = 3.0
rib_spacing = 12.0
rib_height = block_height - 2 * wall_thickness
hole_diameter = 8.0
chamfer_distance = 2.0

base = cq.Workplane('XY').box(block_length, block_width, block_height)

rib_count = int((block_length - 2 * wall_thickness) // rib_spacing) + 1
rib_positions = [ -block_length/2 + wall_thickness + i * rib_spacing for i in range(rib_count) ]

ribs = cq.Workplane('XY')
for x in rib_positions:
    rib = (cq.Workplane('XY')
           .center(x, 0)
           .rect(rib_thickness, block_width - 2 * wall_thickness)
           .extrude(rib_height)
           .translate((0, 0, -block_height/2 + wall_thickness)))
    ribs = ribs.union(rib)

result = base.union(ribs)

result = result.faces('>Z').workplane().hole(hole_diameter)

result = result.edges('|Z').chamfer(chamfer_distance)
