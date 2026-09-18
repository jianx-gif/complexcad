import cadquery as cq

block_length = 80.0
block_width = 50.0
block_height = 20.0
groove_width = 12.0
groove_depth = 5.0
hole_diameter = 6.0
hole_depth = 12.0
hole_spacing = 15.0
num_holes = 3
chamfer_dist = 1.0
rib_height = 5.0
rib_thickness = 3.0
rib_spacing = 20.0

base_sketch = cq.Sketch().rect(block_length, block_width)
result = cq.Workplane('XY').placeSketch(base_sketch).extrude(block_height)

result = result.faces('>Z').workplane().rect(block_length, groove_width).cutBlind(groove_depth)

rib_count = int((block_width - rib_spacing) // rib_spacing) + 1
rib_positions = [(-block_width/2 + rib_spacing/2 + i*rib_spacing) for i in range(rib_count)]
for y in rib_positions:
    rib = cq.Workplane('XY').center(0, y).rect(block_length, rib_thickness).extrude(rib_height)
    result = result.union(rib)

start_x = -((num_holes - 1) * hole_spacing) / 2.0
hole_centers = [(start_x + i * hole_spacing, 0) for i in range(num_holes)]
for cx, cy in hole_centers:
    hole = cq.Workplane('XY').center(cx, cy).circle(hole_diameter/2).extrude(-hole_depth)
    result = result.cut(hole)

result = result.edges('|Z').chamfer(chamfer_dist)
