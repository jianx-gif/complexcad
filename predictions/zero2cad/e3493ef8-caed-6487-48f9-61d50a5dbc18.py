import cadquery as cq

# Parameters
block_length = 80.0
block_width = 60.0
block_thickness = 20.0
rib_width = 20.0
rib_height = 20.0
rib_length = 50.0
hole_diameter = 6.0
hole_depth = 12.0
hole_spacing_x = 30.0
hole_spacing_y = 20.0
fillet_radius = 1.0
chamfer_size = 0.5
mount_hole_diameter = 3.0
mount_hole_offset = 12.0

# Base block
base = cq.Workplane("XY").box(block_length, block_width, block_thickness)

# Central rib on bottom face
rib = (
    base.faces("<Z").workplane()
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)

# Blind holes on top face (2x2 grid)
holes = (
    rib.faces(">Z").workplane()
    .rarray(hole_spacing_x, hole_spacing_y, 2, 2)
    .circle(hole_diameter / 2)
    .cutBlind(hole_depth)
)

# Mounting holes at four corners on top face
mounts = (
    holes.faces(">Z").workplane()
    .rect(block_length - 2 * mount_hole_offset, block_width - 2 * mount_hole_offset, forConstruction=True)
    .vertices()
    .hole(mount_hole_diameter)
)

# Fillet vertical edges
filleted = mounts.edges("|Z").fillet(fillet_radius)

# Chamfer top edges
result = filleted.faces(">Z").chamfer(chamfer_size)
