import cadquery as cq

# Parameters
outer_diameter = 40.0
wall_thickness = 2.0
bellows_length = 80.0
rib_height = 5.0
rib_width = 8.0
rib_thickness = 4.0
rib_pitch = 12.0
num_ribs = int(bellows_length / rib_pitch)
clearance_hole_dia = 10.0
clearance_hole_depth = bellows_length
chamfer_size = 0.5
rib_overlap = 0.5

# Base cylinder and wall
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
base = (
    cq.Workplane('XY')
    .circle(outer_radius)
    .extrude(bellows_length)
    .hole(clearance_hole_dia, clearance_hole_depth)
)
inner_cut = (
    cq.Workplane('XY')
    .circle(inner_radius)
    .extrude(bellows_length)
)
bellows_shell = base.cut(inner_cut)

# Create a single rib profile on XZ plane with overlap into shell
rib_profile = (
    cq.Workplane('XZ')
    .moveTo(outer_radius - rib_overlap, 0)
    .lineTo(outer_radius + rib_height, 0)
    .lineTo(outer_radius + rib_height, rib_width)
    .lineTo(outer_radius - rib_overlap, rib_width)
    .close()
    .extrude(rib_thickness)
)
# Build staggered rib pattern
ribs = cq.Workplane('XY')
for i in range(num_ribs):
    angle = i * (360.0 / num_ribs)
    offset_z = (i % 2) * (rib_pitch / 2.0)
    rib = (
        rib_profile
        .rotate((0,0,0), (0,0,1), angle)
        .translate((0, 0, i * rib_pitch + offset_z))
    )
    ribs = ribs.union(rib)

# Combine ribs with shell, ensuring fusion
bellows_with_ribs = bellows_shell.union(ribs)

# Chamfer outer rib edges for safety
result = (
    bellows_with_ribs
    .edges('>X')
    .chamfer(chamfer_size)
)
