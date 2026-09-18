import cadquery as cq

# Dimensions (max 100 unit scale)
base_width = 80.0
base_height = 30.0
base_thickness = 8.0
base_corner_radius = 3.0
clip_thickness = 3.0
clip_height = 25.0
clip_radius = 5.0
slot_width = 4.0
slot_length = 20.0
slot_spacing = 6.0
num_slots = 4
logo_diameter = 15.0
logo_depth = 2.0
chamfer_dist = 1.0

# Function to create a spring‑clip sweep profile
def make_clip_sweep(thickness, height, radius, sweep_radius):
    left_x = -sweep_radius
    right_x = sweep_radius
    path = (
        cq.Workplane('XY')
        .moveTo(left_x, 0)
        .threePointArc((0, radius), (right_x, 0))
        .wire()
    )
    profile = (
        cq.Workplane('YZ')
        .center(0, -height/2)
        .rect(thickness, height)
    )
    return profile.sweep(path, transition='round')

# Base plate
result = (
    cq.Workplane('XY')
    .rect(base_width, base_height)
    .extrude(base_thickness)
    .edges('|Z')
    .fillet(base_corner_radius)
)

# Clip on right side
clip = (
    make_clip_sweep(clip_thickness, clip_height, clip_radius, clip_radius + clip_thickness)
    .translate((base_width/2 - clip_thickness/2, 0, base_thickness/2))
)
result = result.union(clip)

# Linear slots on top face
slot_pts = [
    (base_width/2 - clip_thickness - slot_length/2, -base_height/2 + slot_spacing + i*slot_spacing)
    for i in range(num_slots)
]
result = (
    result.faces('>Z')
    .workplane()
    .pushPoints(slot_pts)
    .rect(slot_length, slot_width)
    .cutBlind(base_thickness)
)

# Recessed circular logo on opposite edge
result = (
    result.faces('>Z')
    .workplane()
    .center(-base_width/2 + logo_diameter/2 + 5, 0)
    .circle(logo_diameter/2)
    .cutBlind(logo_depth)
)

# Chamfer outer vertical edges of the clip
result = (
    result.edges('>X and |Z')
    .chamfer(chamfer_dist)
)
