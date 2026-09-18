import cadquery as cq

# Parameters
bracket_length = 80.0
bracket_width = 50.0
bracket_thickness = 10.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 4
hole_diameter = 5.0
hole_offset = 10.0
chamfer_size = 1.0
fillet_radius = 0.5

# Base solid
base = cq.Workplane('XY').box(bracket_length, bracket_width, bracket_thickness)

# Shell to create thin walls
shell = base.shell(-wall_thickness)

# Chamfer outer vertical edges
shell = shell.edges('|Z').chamfer(chamfer_size)

# Fillet top outer edges for safety
shell = shell.edges('>Z').fillet(fillet_radius)

# Add ribs on the top face
rib_plane = shell.faces('>Z').workplane()
rib_pattern = rib_plane.rarray(rib_spacing, 0, rib_count, 1, center=True)
ribs = rib_pattern.rect(rib_width, rib_height).extrude(-rib_height)

# Combine ribs with shell
result = shell.union(ribs)

# Drill mounting holes on the +Y side
hole_plane = result.faces('>Y').workplane()
hole_positions = [(-bracket_length/2 + hole_offset, 0), (bracket_length/2 - hole_offset, 0)]
result = hole_plane.pushPoints(hole_positions).hole(hole_diameter)
