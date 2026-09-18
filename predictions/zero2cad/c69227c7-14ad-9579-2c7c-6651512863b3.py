import cadquery as cq
import math

# Parameters
base_diameter = 40.0
base_height = 12.0
shoulder_diameter = 24.0
shoulder_height = 15.0
top_diameter = 34.0
top_height = 10.0
central_hole_diameter = 8.0
mount_hole_diameter = 4.0
mount_hole_count = 4
mount_hole_radius = 15.0
chamfer_distance = 1.0
fillet_radius = 1.0
slot_width = 6.0
slot_length = 20.0
slot_depth = 4.0

# Base cylinder
base = (
    cq.Workplane("XY")
    .circle(base_diameter / 2)
    .extrude(base_height)
)

# Shoulder cylinder (smaller diameter)
shoulder = (
    cq.Workplane("XY")
    .circle(shoulder_diameter / 2)
    .extrude(shoulder_height)
    .translate((0, 0, base_height))
)

# Top cylinder (larger diameter) with slight taper for smooth transition
top = (
    cq.Workplane("XY")
    .circle(top_diameter / 2)
    .extrude(top_height, taper=-10)
    .translate((0, 0, base_height + shoulder_height))
)

# Combine bodies
spacer = base.union(shoulder).union(top)

# Central through hole
spacer = spacer.faces(">Z").workplane().hole(central_hole_diameter)

# Mounting holes on base perimeter
angle_step = 360.0 / mount_hole_count
points = [
    (
        mount_hole_radius * math.cos(math.radians(i * angle_step)),
        mount_hole_radius * math.sin(math.radians(i * angle_step))
    )
    for i in range(mount_hole_count)
]
spacer = (
    spacer.faces("<Z")
    .workplane()
    .pushPoints(points)
    .hole(mount_hole_diameter)
)

# Chamfer on bottom outer edge
spacer = spacer.faces("<Z").edges().chamfer(chamfer_distance)

# Fillet on top outer edge for safety
spacer = spacer.faces(">Z").edges().fillet(fillet_radius)

# Slot on side of base for cable routing
spacer = (
    spacer.faces("<Y")
    .workplane(centerOption="CenterOfMass")
    .rect(slot_length, slot_width)
    .cutBlind(-slot_depth)
)

result = spacer