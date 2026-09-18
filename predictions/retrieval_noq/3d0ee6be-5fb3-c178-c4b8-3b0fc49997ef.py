import cadquery as cq
import math
body_diameter_outer = 80.0
body_length = 70.0
inlet_diameter = 30.0
outlet_diameter = 30.0
step_diameter = 40.0
step_length = 20.0
flange_thickness = 5.0
flange_diameter = 100.0
relief_hole_diameter = 5.0
relief_hole_depth = 10.0
relief_hole_count = 8
mount_hole_diameter = 6.0
mount_hole_offset = 15.0
chamfer_size = 2.0
outer_radius = body_diameter_outer / 2.0
flange_radius = flange_diameter / 2.0
wall_thickness = outer_radius - step_diameter / 2.0
profile = (
    cq.Workplane("XZ")
    .lineTo(flange_radius, 0)
    .lineTo(flange_radius, -flange_thickness)
    .lineTo(outer_radius, -flange_thickness)
    .lineTo(outer_radius, -(flange_thickness + body_length))
    .lineTo(0, -(flange_thickness + body_length))
    .close()
)
outer_solid = profile.revolve()
inner_profile = (
    cq.Workplane("XZ")
    .lineTo(inlet_diameter / 2.0, 0)
    .lineTo(inlet_diameter / 2.0, -(flange_thickness + body_length - step_length))
    .lineTo(step_diameter / 2.0, -(flange_thickness + body_length - step_length))
    .lineTo(step_diameter / 2.0, -(flange_thickness + body_length))
    .lineTo(0, -(flange_thickness + body_length))
    .close()
)
inner_solid = inner_profile.revolve()
result = outer_solid.cut(inner_solid)
for i in range(relief_hole_count):
    angle = 2 * math.pi * i / relief_hole_count
    radial_dist = outer_radius - relief_hole_depth / 2.0
    hole = (
        cq.Workplane("YZ")
        .circle(relief_hole_diameter / 2.0)
        .extrude(relief_hole_depth)
        .rotate((0, 0, 0), (0, 0, 1), math.degrees(angle))
        .translate((radial_dist * math.cos(angle), radial_dist * math.sin(angle), 0))
    )
    result = result.cut(hole)
mount_positions = [
    (mount_hole_offset, mount_hole_offset),
    (-mount_hole_offset, mount_hole_offset),
    (mount_hole_offset, -mount_hole_offset),
    (-mount_hole_offset, -mount_hole_offset),
]
for x, y in mount_positions:
    result = result.faces("<Z").workplane().center(x, y).hole(mount_hole_diameter)
result = result.edges("|Z").chamfer(chamfer_size)
