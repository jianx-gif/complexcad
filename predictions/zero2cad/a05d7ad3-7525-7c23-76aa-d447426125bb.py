import cadquery as cq
import math

outer_diameter = 80.0
plate_thickness = 5.0
central_hole_diameter = 20.0
central_hole_depth = 3.0
fillet_radius = 2.0
mount_hole_diameter = 5.0
mount_hole_count = 4
mount_hole_radius = 30.0
rib_width = 4.0
rib_height = 2.0
rib_count = 6
rib_offset = 5.0
vent_hole_diameter = 4.0
vent_hole_count = 8
vent_hole_radius = 35.0

base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(plate_thickness)
)

base = base.edges().fillet(fillet_radius)

base = (
    base.faces(">Z")
    .workplane()
    .circle(central_hole_diameter / 2)
    .cutBlind(central_hole_depth)
)

angle_step = 360.0 / mount_hole_count
for i in range(mount_hole_count):
    theta = math.radians(i * angle_step)
    x = mount_hole_radius * math.cos(theta)
    y = mount_hole_radius * math.sin(theta)
    base = (
        base.faces(">Z")
        .workplane()
        .center(x, y)
        .hole(mount_hole_diameter)
    )

rib_angle_step = 360.0 / rib_count
for i in range(rib_count):
    theta = math.radians(i * rib_angle_step)
    x = (outer_diameter / 2 - rib_offset - rib_width / 2) * math.cos(theta)
    y = (outer_diameter / 2 - rib_offset - rib_width / 2) * math.sin(theta)
    rib = (
        cq.Workplane("XY")
        .center(x, y)
        .rect(rib_width, rib_height)
        .extrude(plate_thickness)
    )
    base = base.union(rib)

vent_angle_step = 360.0 / vent_hole_count
for i in range(vent_hole_count):
    theta = math.radians(i * vent_angle_step)
    x = vent_hole_radius * math.cos(theta)
    y = vent_hole_radius * math.sin(theta)
    base = (
        base.faces(">Z")
        .workplane()
        .center(x, y)
        .hole(vent_hole_diameter)
    )

result = base