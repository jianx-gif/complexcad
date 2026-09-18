import cadquery as cq

# Parameters
outer_diameter = 60.0
cap_height = 30.0
wall_thickness = 3.0
tab_width = 20.0
tab_height = 10.0
tab_thickness = 4.0
chamfer_size = 1.0
thread_diameter = 15.0
thread_length = 12.0
thread_pitch = 2.0
thread_depth = 0.8

# Base cylinder
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(cap_height)
# Shell to create wall thickness
hollow = base.shell(-wall_thickness)
# Add side tab (rectangular protrusion)
# Position tab on +X side, centered vertically
tab = (
    cq.Workplane('XY')
    .center(0, outer_diameter/2 + tab_thickness/2)
    .rect(tab_width, tab_height)
    .extrude(tab_thickness)
)
# Combine tab with hollow body
combined = hollow.union(tab)
# Chamfer top outer edge
combined = combined.faces('>Z').edges().chamfer(chamfer_size)
# Threaded insert cavity (blind hole)
# Create a blind hole for the insert
cavity = (
    cq.Workplane('XY')
    .center(0, 0)
    .circle(thread_diameter/2)
    .extrude(thread_length)
)
# Subtract cavity from combined part
result = combined.cut(cavity)
# Add internal thread geometry (triangular profile swept along helix)
# Define triangular thread profile
thread_profile = (
    cq.Workplane('XZ')
    .polyline([
        (0, 0),
        (thread_depth, thread_pitch/2),
        (0, thread_pitch)
    ])
    .close()
)
# Define helix path for thread
helix_path = cq.Wire.makeHelix(pitch=thread_pitch, height=thread_length, radius=thread_diameter/2 - thread_depth)
# Sweep profile along helix to create thread solid
thread_solid = thread_profile.sweep(helix_path)
# Cut thread from the cavity to create internal threads
result = result.cut(thread_solid)
