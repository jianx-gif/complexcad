import cadquery as cq

# Parameters
block_length = 80.0
block_width = 60.0
block_thickness = 12.0
keyway_length = 60.0
keyway_width = 20.0
keyway_depth = 4.0
hole_diameter = 6.0
hole_offset = 12.0
chamfer_size = 1.0
rib_height = 3.0
rib_thickness = 4.0
rib_spacing = 15.0

# Base block with chamfered top edges
base = (
    cq.Workplane("XY")
    .box(block_length, block_width, block_thickness)
    .faces(">Z")
    .edges()
    .chamfer(chamfer_size)
)

# Recessed keyway on top surface
keyway = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(keyway_length, keyway_width)
    .cutBlind(-keyway_depth)
)

# Four M6 through holes near corners
holes = (
    keyway.faces(">Z").workplane()
    .rect(block_length - 2 * hole_offset, block_width - 2 * hole_offset, forConstruction=True)
    .vertices()
    .hole(hole_diameter)
)

# Underside ribs for stiffness (grid pattern)
rib_grid = (
    holes.faces("<Z").workplane()
    .rarray(rib_spacing, rib_spacing, int(block_length / rib_spacing), int(block_width / rib_spacing))
    .rect(rib_thickness, rib_thickness)
    .extrude(-rib_height)
)

result = rib_grid
