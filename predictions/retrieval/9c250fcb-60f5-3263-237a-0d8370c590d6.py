import cadquery as cq

# Parameters
block_length = 80.0
block_width = 50.0
block_height = 15.0
pocket_length = 40.0
pocket_width = 20.0
pocket_offset_x = 10.0
pocket_offset_y = 15.0
pocket_depth = 10.0
hole_diameter = 12.0
hole_offset_x = 30.0
hole_offset_y = 0.0
chamfer_dist = 1.0
rib_depth = 4.0
rib_height = 5.0
mount_hole_dia = 5.0
mount_hole_spacing = 30.0
mount_hole_offset_y = 10.0

# Base block sketch: main rectangle with a subtractive slot
base_sketch = cq.Sketch().rect(block_length, block_width, mode='a')
base_sketch = base_sketch.slot(15, 5, mode='s')
result = cq.Workplane('XY').placeSketch(base_sketch).extrude(block_height)
result = result.edges().chamfer(chamfer_dist)

# Pocket cut on top face
result = result.faces('>Z').workplane().center(pocket_offset_x, pocket_offset_y).rect(pocket_length, pocket_width).cutBlind(-pocket_depth)

# Through hole on top face
result = result.faces('>Z').workplane().center(hole_offset_x, hole_offset_y).hole(hole_diameter)

# Mounting holes pattern on top face
mount_pts = [(-mount_hole_spacing/2, mount_hole_offset_y), (mount_hole_spacing/2, mount_hole_offset_y)]
result = result.faces('>Z').workplane().pushPoints(mount_pts).hole(mount_hole_dia)

# Rib slots on +X and -X side faces (cut into the block)
result = result.faces('>X').workplane().center(0, rib_height/2).rect(rib_depth, rib_height).cutBlind(-rib_depth)
result = result.faces('<X').workplane().center(0, rib_height/2).rect(rib_depth, rib_height).cutBlind(-rib_depth)
