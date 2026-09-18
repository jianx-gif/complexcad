import cadquery as cq

outer_size = 80.0
wall_thickness = 2.0
channel_length = 100.0
rib_width = 10.0
rib_height = 5.0
countersink_angle = 90.0
countersink_diameter = 5.5
hole_diameter = 3.2
hole_spacing = 25.0
holes_per_side = 3
chamfer_distance = 1.0

# Base square channel with thin walls
base = (
    cq.Workplane('XY')
    .rect(outer_size, outer_size)
    .extrude(channel_length)
    .shell(-wall_thickness, kind='intersection')
)

# Add external ribs on the top face for stiffness
ribbed = (
    base.faces('>Z')
    .workplane()
    .rect(outer_size, rib_width)
    .extrude(rib_height, combine=True)
)

# Countersunk holes on the right side (+X)
right_side_holes = (
    ribbed.faces('>X')
    .workplane()
    .rarray(0, hole_spacing, 1, holes_per_side)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle, wall_thickness + rib_height)
)

# Countersunk holes on the left side (-X)
left_side_holes = (
    right_side_holes.faces('<X')
    .workplane()
    .rarray(0, hole_spacing, 1, holes_per_side)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle, wall_thickness + rib_height)
)

# Chamfer outer edges for safety
result = (
    left_side_holes
    .edges('|Z or >X or <X')
    .chamfer(chamfer_distance)
)
