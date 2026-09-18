import cadquery as cq

# Parameters
block_length = 80.0
block_width = 50.0
block_height = 30.0
rib_width = 6.0
rib_spacing = 10.0
rib_height = 5.0
central_hole_diameter = 8.0
thread_pitch = 2.0
thread_depth = 2.0
corner_chamfer = 2.0

# Base block
base = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_height)
    .edges("|Z")
    .chamfer(corner_chamfer)
)

# Rib grid on top face
num_ribs_x = int((block_length - 2 * rib_spacing) // (rib_width + rib_spacing))
rib_union = cq.Workplane("XY")
for i in range(num_ribs_x):
    offset_x = -block_length / 2 + rib_spacing + i * (rib_width + rib_spacing) + rib_width / 2
    rib = (
        cq.Workplane("XY")
        .center(offset_x, 0)
        .rect(rib_width, block_width - 2 * rib_spacing)
        .extrude(rib_height)
    )
    rib_union = rib_union.union(rib)

combined = base.union(rib_union)
combined = combined.faces(">Z").workplane().hole(central_hole_diameter)

# Thread creation using helix sweep
helix_height = block_height - 2 * corner_chamfer
helix_radius = (central_hole_diameter / 2) - thread_depth
helix = cq.Wire.makeHelix(pitch=thread_pitch, height=helix_height, radius=helix_radius)

thread_profile = (
    cq.Workplane()
    .polyline([[0, 0], [thread_pitch / 2, thread_depth], [thread_pitch, 0]])
    .close()
    .translate((helix_radius, 0, 0))
)

thread_solid = thread_profile.sweep(path=helix, makeSolid=True)

result = combined.cut(thread_solid)
