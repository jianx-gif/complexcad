import cadquery as cq
import math

# Parameters
base_radius = 20.0
base_height = 15.0
arm_length = 70.0
arm_outer_radius = 30.0
arm_taper_angle = 5.0
central_hole_diameter = 10.0
mount_hole_diameter = 6.0
mount_hole_offset = 12.0
rib_count = 6
rib_width = 5.0
rib_height = 30.0
rib_thickness = 2.0
chamfer_size = 0.5

# Base cylinder
base = cq.Workplane("XY").circle(base_radius).extrude(base_height)

# Tapered arm using extrude with taper
arm = (
    cq.Workplane("XY", origin=(0, 0, base_height))
    .circle(arm_outer_radius)
    .extrude(arm_length, taper=arm_taper_angle)
)

# Combine base and arm
result = base.union(arm)

# Central through hole
result = result.faces(">Z").workplane().hole(central_hole_diameter)

# Mounting holes on base (four around perimeter)
mount_radius = base_radius - mount_hole_offset
mount_points = [
    (mount_radius * math.cos(math.radians(a)), mount_radius * math.sin(math.radians(a)))
    for a in (0, 90, 180, 270)
]
result = result.faces("<Z").workplane().pushPoints(mount_points).hole(mount_hole_diameter)

# Add ribs around arm
for i in range(rib_count):
    angle = i * 360.0 / rib_count
    rib = (
        cq.Workplane("XY")
        .box(rib_thickness, rib_width, rib_height)
        .translate((arm_outer_radius - rib_thickness / 2, 0, base_height + rib_height / 2))
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.union(rib)

# Chamfer top edges for safety
result = result.faces(">Z").edges().chamfer(chamfer_size)
