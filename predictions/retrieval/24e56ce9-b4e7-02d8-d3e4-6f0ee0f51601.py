import cadquery as cq

# Parameters (max dimension 100 units convention)
large_diameter = 80.0
small_diameter = 40.0
length_cone = 80.0
wall_thickness = 3.0
chamfer_size = 1.0
thread_pitch = 2.5
thread_length = 30.0

# Derived dimensions
large_radius = large_diameter / 2.0
small_radius = small_diameter / 2.0
boss_radius = small_radius - wall_thickness
thread_height = boss_radius * 0.1  # approximate thread depth

# 1. Base conical reducer solid (triangular profile) and revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(large_radius, 0)
    .lineTo(small_radius, length_cone)
    .close()
)
cone = profile.revolve(360)

# 2. Shell to create thin-walled reducer
shelled = cone.shell(-wall_thickness)

# 3. Chamfer outer edge at large end for safety
shelled = shelled.edges("(>Z and >Y)").chamfer(chamfer_size)

# 4. Add cylindrical boss for threading at the small end
boss_height = thread_length + 5.0
shelled = (
    shelled.faces(">Z").workplane()
    .circle(boss_radius)
    .extrude(boss_height)
)

# 5. Triangular thread profile (2D) for sweep
thread_profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .line(thread_pitch / 2.0, thread_height)
    .line(thread_pitch / 2.0, -thread_height)
    .close()
)

# 6. Helical wire for thread (using Wire.makeHelix)
helix_wire = cq.Wire.makeHelix(pitch=thread_pitch, height=thread_length, radius=boss_radius)
helix_wire = helix_wire.translate((0, 0, length_cone))

# 7. Sweep thread profile along helix to create thread solid
thread_solid = thread_profile.sweep(helix_wire)

# 8. Cut thread from boss to create male threads
result = shelled.cut(thread_solid)
