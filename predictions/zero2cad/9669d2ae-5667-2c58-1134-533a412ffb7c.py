import cadquery as cq

# Parameters
outer_radius = 45.0
inner_radius = 30.0
wall_thickness = 5.0
height = 30.0
lip_height = 4.0
lip_thickness = 2.0
chamfer_size = 1.0
thread_diameter = 6.0
thread_length = 20.0
thread_pitch = 2.0
thread_profile_width = 1.2
thread_profile_height = 0.8

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, height - lip_height)
    .lineTo(outer_radius - lip_thickness, height - lip_height)
    .threePointArc((outer_radius, height - lip_height + lip_thickness / 2), (outer_radius, height))
    .lineTo(outer_radius, 0)
    .close()
)

# Revolve to create solid
solid = profile.revolve()

# Shell to create hollow interior
hollow = solid.shell(-wall_thickness)

# Chamfer outer lip edge (top outer edge)
chamfered = hollow.edges(">Z").chamfer(chamfer_size)

# Threaded insert hole (cylindrical cut)
hole = (
    cq.Workplane("XZ")
    .center(0, 0)
    .circle(thread_diameter / 2)
    .extrude(thread_length)
)

# Thread profile (triangular) for internal thread
thread_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(thread_profile_width / 2, thread_profile_height)
    .lineTo(-thread_profile_width / 2, thread_profile_height)
    .close()
)

# Helix path for thread using Wire.makeHelix
helix_path = cq.Wire.makeHelix(pitch=thread_pitch, height=thread_length, radius=thread_diameter / 2)

# Sweep thread profile along helix to create thread solid
thread_solid = thread_profile.sweep(helix_path)

# Cut thread from hole
threaded_hole = hole.cut(thread_solid)

# Subtract threaded hole from part
result = chamfered.cut(threaded_hole)
