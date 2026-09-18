import cadquery as cq
import math

# Parameters
outer_diameter = 70.0
inner_diameter = 30.0
reduced_diameter = 50.0
base_length = 40.0
top_length = 20.0
total_length = base_length + top_length
sensor_pocket_diameter = 20.0
sensor_pocket_depth = 15.0
mount_hole_diameter = 6.0
mount_hole_count = 4
mount_hole_radius = (inner_diameter/2 + outer_diameter/2) / 2
chamfer_size = 2.0

# Base profile (non‑trivial with two radii)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_diameter/2, 0)
    .lineTo(outer_diameter/2, base_length)
    .lineTo(reduced_diameter/2, base_length)
    .lineTo(reduced_diameter/2, total_length)
    .lineTo(0, total_length)
    .close()
)

# Revolve to create housing
housing = profile.revolve()

# Central through‑hole
through_hole = (
    cq.Workplane("XY")
    .circle(inner_diameter/2)
    .extrude(total_length)
)
housing = housing.cut(through_hole)

# Blind sensor pocket (cylindrical pocket on side of reduced section)
# Create pocket cylinder oriented radially inward
pocket_cyl = (
    cq.Workplane("XY")
    .circle(sensor_pocket_diameter/2)
    .extrude(sensor_pocket_depth)
    .rotate((0, 0, 0), (0, 1, 0), 90)
    .translate((reduced_diameter/2, total_length - sensor_pocket_depth/2, 0))
)
housing = housing.cut(pocket_cyl)

# Mounting holes on top face, drilled through Z direction
hole_positions = []
for i in range(mount_hole_count):
    angle = i * 360.0 / mount_hole_count
    rad = math.radians(angle)
    x = mount_hole_radius * math.cos(rad)
    y = mount_hole_radius * math.sin(rad)
    hole_positions.append((x, y))

housing = (
    housing
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_diameter)
)

# Chamfer entrance edge (top outer edge)
result = housing.edges(">Z").chamfer(chamfer_size)
