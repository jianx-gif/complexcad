import cadquery as cq

# Parameters
channel_length = 80.0
channel_width = 40.0
channel_height = 30.0
wall_thickness = 3.0
rib_thickness = 2.0
rib_height = 10.0
rib_spacing = 12.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 30.0

# Base solid
base = cq.Workplane('XY').box(channel_length, channel_width, channel_height)

# Create hollow channel via shell
hollow = base.shell(wall_thickness)

# Chamfer outer edges for safety
hollow = hollow.edges('|Z').chamfer(chamfer_size)

# Add mounting holes on the +Y side
hollow = (
    hollow.faces('>Y')
    .workplane()
    .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
    .hole(hole_diameter)
)

# Internal rib dimensions
rib_length = channel_length - 2 * wall_thickness
rib_width = channel_width - 2 * wall_thickness

# Create a single rib solid
rib = (
    cq.Workplane('XY')
    .box(rib_length, rib_width, rib_height)
    .translate((0, 0, -channel_height/2 + wall_thickness + rib_height/2))
)

# Determine number of ribs based on spacing
num_ribs = int((channel_length - 2 * wall_thickness) // rib_spacing) + 1

# Assemble ribs in a linear array along X
ribs = rib
for i in range(1, num_ribs):
    offset = -channel_length/2 + wall_thickness + i * rib_spacing
    ribs = ribs.union(rib.translate((offset, 0, 0)))

# Combine ribs with hollow channel
result = hollow.union(ribs)
