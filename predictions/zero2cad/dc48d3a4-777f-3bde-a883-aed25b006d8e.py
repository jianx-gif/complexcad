import cadquery as cq
import math

# Parameters
body_diameter = 80.0
body_length = 70.0
inlet_diameter = 30.0
inlet_length = 30.0
wall_thickness = 5.0
chamfer_size = 2.0
mount_hole_diameter = 5.0
mount_hole_count = 4
mount_hole_radius = 30.0
rib_radius = 4.0
rib_height = 20.0
rib_count = 6
rib_spacing_angle = 360.0 / rib_count
thread_hole_diameter = 8.0

# Derived dimensions
body_radius = body_diameter / 2.0
inlet_radius = inlet_diameter / 2.0
inlet_start_z = body_length - inlet_length

# Base valve body profile (XZ plane) and revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(body_radius, 0)
    .lineTo(body_radius, inlet_start_z)
    .threePointArc((body_radius + 5, inlet_start_z + 5), (inlet_radius, inlet_start_z + inlet_length))
    .lineTo(0, body_length)
    .close()
)
valve_body = profile.revolve()

# Chamfer inlet edge (bottom face)
valve_body = valve_body.faces("<Z").edges().chamfer(chamfer_size)

# Mounting holes on top face, arranged circularly
valve_body = (
    valve_body.faces(">Z")
    .workplane()
    .polarArray(radius=mount_hole_radius, startAngle=0, angle=360, count=mount_hole_count)
    .hole(mount_hole_diameter)
)

# Internal ribs (cylindrical bosses) evenly spaced around interior
rib = (
    cq.Workplane("XY")
    .circle(rib_radius)
    .extrude(rib_height)
)
for i in range(rib_count):
    angle = i * rib_spacing_angle
    positioned_rib = (
        rib.rotate((0, 0, 0), (0, 0, 1), angle)
        .translate((0, 0, inlet_start_z + inlet_length / 2.0))
    )
    valve_body = valve_body.union(positioned_rib)

# Central threaded hole (simple through hole) on top face
valve_body = valve_body.faces(">Z").workplane().hole(thread_hole_diameter)

result = valve_body