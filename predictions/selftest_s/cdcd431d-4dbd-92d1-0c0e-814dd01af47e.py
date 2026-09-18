import cadquery as cq
import math

# Parameters
bore_diameter = 20.0
outer_diameter = 44.0
collar_thickness = 12.0
set_screw_diameter = 5.0
set_screw_head_diameter = 9.0
set_screw_angle = 0.0
set_screw_depth = collar_thickness
chamfer_distance = 0.7
relief_width = 4.0
relief_depth = 2.0
relief_offset = 5.0
vent_radius = 6.0
vent_depth = collar_thickness / 3.0
rib_thickness = 2.0
rib_height = collar_thickness * 0.8
rib_width = outer_diameter * 0.1
csk_depth = 1.5
csk_angle = 90.0

bore_radius = bore_diameter / 2.0
outer_radius = outer_diameter / 2.0
relief_half_width = relief_width / 2.0

# Base collar profile (XZ plane) and revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(bore_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, collar_thickness)
    .lineTo(bore_radius, collar_thickness)
    .close()
)
collar = profile.revolve()

# Chamfer outer rim (apply to all external edges for robustness)
collar = collar.edges().chamfer(chamfer_distance)

# Set‑screw clearance hole (through the wall)
set_screw_center_radius = bore_radius + (outer_radius - bore_radius) / 2.0
set_screw_x = set_screw_center_radius * math.cos(math.radians(set_screw_angle))
set_screw_y = set_screw_center_radius * math.sin(math.radians(set_screw_angle))
collar = (
    collar.faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .center(set_screw_x, set_screw_y)
    .hole(set_screw_diameter, depth=set_screw_depth)
)

# Countersunk recess for set‑screw head
collar = (
    collar.faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .center(set_screw_x, set_screw_y)
    .cskHole(set_screw_head_diameter, set_screw_diameter, depth=csk_depth, cskAngle=csk_angle)
)

# Relief slot on inner side for stress relief
relief_angle = 45.0
relief_center_radius = bore_radius + relief_offset
relief_x = relief_center_radius * math.cos(math.radians(relief_angle))
relief_y = relief_center_radius * math.sin(math.radians(relief_angle))
collar = (
    collar.faces("<Z")
    .workplane(centerOption="CenterOfMass")
    .center(relief_x, relief_y)
    .rect(relief_width, relief_depth)
    .cutBlind(-collar_thickness / 2)
)

# Vent pocket on back side for weight reduction
collar = (
    collar.faces("<Z")
    .workplane(centerOption="CenterOfMass")
    .center(0, 0)
    .circle(vent_radius)
    .cutBlind(-vent_depth)
)

# Reinforcing rib on outer face
rib = (
    cq.Workplane("XY")
    .center(0, outer_radius - rib_thickness / 2)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
    .translate((0, 0, collar_thickness / 2 - rib_height / 2))
)

result = collar.union(rib)
