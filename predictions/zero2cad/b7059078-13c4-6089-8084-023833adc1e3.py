import cadquery as cq
import math

# Parameters
cap_height = 40.0
outer_radius_bottom = 30.0
outer_radius_top = 20.0
wall_thickness = 4.0
inner_radius_bottom = outer_radius_bottom - wall_thickness
inner_radius_top = outer_radius_top - wall_thickness
fillet_radius = 1.5
chamfer_distance = 1.0
mount_hole_diameter = 4.0
mount_hole_count = 4
mount_hole_radius = 22.0
rib_thickness = 2.0
rib_height = 10.0
rib_count = 6
rib_angle_step = 360.0 / rib_count

# Base profile for revolve (outer and inner walls)
profile = (
    cq.Workplane("XY")
    .moveTo(outer_radius_bottom, 0)
    .lineTo(outer_radius_top, cap_height)
    .lineTo(inner_radius_top, cap_height)
    .lineTo(inner_radius_bottom, 0)
    .close()
)

# Revolve to create hollow conical cap
result = profile.revolve()

# Chamfer bottom outer edge for safety
result = result.faces("<Z").edges().chamfer(chamfer_distance)

# Fillet all edges for smooth transition
result = result.edges().fillet(fillet_radius)

# Add mounting holes on top face arranged in a circle
hole_positions = []
for i in range(mount_hole_count):
    angle = i * 360.0 / mount_hole_count
    x = mount_hole_radius * math.cos(math.radians(angle))
    y = mount_hole_radius * math.sin(math.radians(angle))
    hole_positions.append((x, y))
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_diameter)
)

# Add internal ribs for stiffness (radial ribs inside the cap)
for i in range(rib_count):
    angle = i * rib_angle_step
    rib = (
        cq.Workplane("XY")
        .center(inner_radius_bottom + wall_thickness/2, 0)
        .rect(rib_thickness, rib_height)
        .extrude(wall_thickness)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.union(rib)
