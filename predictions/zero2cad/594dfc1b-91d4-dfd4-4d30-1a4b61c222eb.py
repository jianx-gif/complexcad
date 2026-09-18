import cadquery as cq
import math

# Parameters
base_radius = 30.0
base_height = 15.0
taper_height = 20.0
top_radius = 22.0
top_height = 8.0
wall_thickness = 3.0
mount_hole_diameter = 5.0
mount_hole_count = 4
mount_hole_radius = base_radius - wall_thickness - 5.0
chamfer_size = 1.0

# Helper to get first solid
def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

# Build profile for revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, base_height)
    .lineTo(top_radius, base_height + taper_height)
    .lineTo(top_radius, base_height + taper_height + top_height)
    .lineTo(0, base_height + taper_height + top_height)
    .close()
)

# Revolve to create knob body
knob_body = (
    profile
    .revolve(360)
    .firstSolid()
    .edges("<Z")
    .chamfer(chamfer_size)
)

# Add mounting holes on base
hole_positions = [
    (
        mount_hole_radius * math.cos(2 * math.pi * i / mount_hole_count),
        mount_hole_radius * math.sin(2 * math.pi * i / mount_hole_count)
    )
    for i in range(mount_hole_count)
]

result = (
    knob_body
    .faces("<Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_diameter)
)
