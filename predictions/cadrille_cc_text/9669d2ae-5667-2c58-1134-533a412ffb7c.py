import cadquery as cq
import math
arm_arm_length = 60.0
arm_arm_length = 80.0
arm_arm_length = 10.0
arm_arm_length = arm_thickness
outer_corner_radius = 5.0
outer_corner_radius = outer_corner_radius - outer_corner_radius
outer_radius = outer_corner_radius - outer_corner_radius
outer_radius = outer_corner_radius - outer_corner_radius
slot_width = 7.0
slot_length = 20.0
rib_width = 6.0
rib_height = 10.0
rib_depth = 8.0
rib_count = 4
base = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, arm_thickness)
    .lineTo(outer_radius + arm_thickness, arm_thickness)
    .lineTo(outer_radius + arm_thickness, arm_thickness + arm_length)
    .lineTo(outer_radius, arm_thickness + arm_length)
    .lineTo(outer_radius, 0)
    .close()
)
base = base.cut(slot)
base = base.edges().chamfer(outer_corner_radius)
slot = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(slot_width, slot_length)
    .extrude(arm_arm_length)
)
base = base.cut(slot)
base = base.edges().chamfer(outer_corner_radius)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_depth)
)
base = base.union(rib)
slot = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(slot_length, slot_width)
    .extrude(outer_radius + 2)
)
result = base.cut(slot)
