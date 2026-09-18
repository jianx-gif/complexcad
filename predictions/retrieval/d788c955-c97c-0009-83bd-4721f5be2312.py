import cadquery as cq

# Parameters
bellows_length = 80.0
num_convolutions = 5
base_radius = 20.0
amplitude = 4.0
shell_thickness = 1.0
rib_height = 8.0
rib_clearance = 0.5
rib_radius = base_radius - shell_thickness - rib_clearance
base_thickness = 6.0
base_plate_radius = base_radius + 5.0
chamfer_size = 0.5
overlap = 0.4

# Derived dimensions
half_wave_len = bellows_length / (num_convolutions * 2)

# Build central wave profile points
wave_pts = [(0, base_radius)]
for i in range(1, num_convolutions * 2):
    x = i * half_wave_len
    r = base_radius + amplitude if i % 2 == 1 else base_radius - amplitude
    wave_pts.append((x, r))
wave_pts.append((bellows_length, base_radius))

# Create bellows solid by revolve and shell
profile = cq.Workplane('XZ')
profile = profile.moveTo(0, 0)
profile = profile.lineTo(0, base_radius)
for pt in wave_pts[1:]:
    profile = profile.lineTo(pt[0], pt[1])
profile = profile.lineTo(bellows_length, 0)
profile = profile.close()
bellows_solid = profile.revolve()
thin_bellows = bellows_solid.shell(-shell_thickness)

# Internal rib (cylinder along X axis)
rib = (
    cq.Workplane()
    .center(bellows_length / 2, 0)
    .cylinder(rib_height, rib_radius)
    .rotate((0, 0, 0), (0, 1, 0), 90)
)

# Base plate (flange) attached to front of bellows with slight overlap
plate_center_x = -base_thickness / 2 + overlap / 2
plate = (
    cq.Workplane()
    .cylinder(base_thickness, base_plate_radius)
    .rotate((0, 0, 0), (0, 1, 0), 90)
    .translate((plate_center_x, 0, 0))
)

# Assemble components into a single solid
result = thin_bellows.union(rib).union(plate)
# Chamfer front edge of plate for safety
result = result.faces('>X').edges().chamfer(chamfer_size)
