import cadquery as cq

# Parameters
outer_diameter = 40.0
wall_thickness = 4.0
bellows_length = 80.0
corrugation_count = 6
corrugation_amplitude = 3.0
rib_height = 2.0
rib_width = 4.0
rib_pitch = 10.0
chamfer_size = 1.0

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
corrugation_pitch = bellows_length / corrugation_count

# Build bellows profile points (XZ plane)
points = []
points.append((inner_radius, 0.0))
points.append((outer_radius, 0.0))
for i in range(corrugation_count):
    z_start = i * corrugation_pitch
    z_mid = z_start + corrugation_pitch / 2.0
    z_end = (i + 1) * corrugation_pitch
    points.append((outer_radius + corrugation_amplitude, z_mid))
    points.append((outer_radius, z_end))
points.append((inner_radius, bellows_length))

# Create bellows by revolving the profile
bellows = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve()
)

# Helical rib using Wire.makeHelix
helix_path = cq.Wire.makeHelix(pitch=rib_pitch, height=bellows_length, radius=outer_radius + rib_height / 2.0)
rib_profile = cq.Workplane("XY").rect(rib_width, rib_height)
rib = rib_profile.sweep(helix_path)

# Combine bellows and rib
combined = bellows.union(rib)

# Apply chamfer to the start face (Z=0)
result = combined.faces("<Z").edges().chamfer(chamfer_size)
