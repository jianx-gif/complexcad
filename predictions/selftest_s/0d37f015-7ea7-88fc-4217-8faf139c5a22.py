import cadquery as cq
import math

# Parameters
body_diameter = 40.0
body_height = 70.0
flange_thickness = 10.0
flange_diameter = 60.0
flange_pocket_diameter = 30.0
flange_pocket_depth = 6.0
mount_hole_diameter = 4.0
mount_hole_radius = 20.0
mount_hole_count = 4
lead = 20.0
starts = 12
thread_depth = 4.0
thread_width = 3.0
edge_chamfer = 0.7

# Core cylinder (without flange)
core_cyl = (
    cq.Workplane("XY")
    .circle(body_diameter / 2)
    .extrude(body_height - flange_thickness)
)

# Single thread helix (one start)
thread_profile = (
    cq.Workplane("XZ")
    .moveTo(body_diameter / 2 - thread_depth, 0)
    .lineTo(body_diameter / 2 - thread_depth + thread_width, 0)
    .lineTo(body_diameter / 2, thread_depth)
    .close()
    .twistExtrude(lead, 360)
)

# Replicate thread for multiple starts
threads = cq.Workplane("XY").union(thread_profile)
for i in range(1, starts):
    angle = i * 360.0 / starts
    threads = threads.union(thread_profile.rotate((0, 0, 0), (0, 0, 1), angle))

# Mounting flange with recessed pocket and mounting holes
flange = (
    cq.Workplane("XY")
    .circle(flange_diameter / 2)
    .extrude(flange_thickness)
)

pocket = (
    cq.Workplane("XY")
    .circle(flange_pocket_diameter / 2)
    .extrude(flange_pocket_depth)
    .translate((0, 0, flange_thickness - flange_pocket_depth))
)

flange_with_pocket = flange.cut(pocket)

hole_positions = []
for i in range(mount_hole_count):
    ang = math.radians(i * 360.0 / mount_hole_count)
    hole_positions.append((mount_hole_radius * math.cos(ang), mount_hole_radius * math.sin(ang)))

flange_holes = (
    flange_with_pocket.workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_diameter)
)

# Apply chamfer to outer cylindrical edges of flange for safety
flange_final = flange_holes.edges(">Z").chamfer(edge_chamfer)

# Assemble final part
result = core_cyl.union(threads).union(flange_final)
