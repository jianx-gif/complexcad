import cadquery as cq

# Parameters
block_length = 80.0
block_width = 40.0
block_height = 20.0
wall_thickness = 4.0
bearing_diameter = 15.0
bearing_length = 30.0
bearing_offset = 10.0
keyway_width = 6.0
keyway_depth = 4.0
keyway_length = 20.0
vent_hole_diameter = 4.0
vent_rows = 4
vent_cols = 6
vent_spacing_x = 10.0
vent_spacing_y = 6.0
chamfer_size = 0.8

# Base block
result = (
    cq.Workplane("XY")
    .rect(block_width, block_length)
    .extrude(block_height)
)

# Bearing seat cut (cylindrical pocket)
bearing_center_y = block_length / 2 - bearing_offset - bearing_length / 2
bearing_cut = (
    cq.Workplane("XY")
    .center(0, bearing_center_y)
    .circle(bearing_diameter / 2)
    .extrude(block_height)
)
result = result.cut(bearing_cut)

# Keyway cut (rectangular slot on side)
keyway_center_y = block_length / 2 - bearing_offset - bearing_length - keyway_length / 2
keyway_cut = (
    cq.Workplane("XY")
    .center(0, keyway_center_y)
    .rect(keyway_width, keyway_length)
    .extrude(keyway_depth)
)
result = result.cut(keyway_cut)

# Vent holes pattern on front face (+Y)
result = (
    result.faces(">Y")
    .workplane()
    .rarray(vent_spacing_x, vent_spacing_y, vent_cols, vent_rows)
    .hole(vent_hole_diameter)
)

# Chamfer outer vertical edges for safety
result = result.edges("|Z").chamfer(chamfer_size)
