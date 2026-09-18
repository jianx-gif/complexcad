import cadquery as cq
import math
base_radius = 40.0
wall_thickness = 2.0
tip_radius = 1.0
vent_slot_width = 4.0
vent_slot_height = 12.0
vent_slot_offset = 15.0
vent_count = 8
vent_slot_depth = wall_thickness + 2.0
mount_hole_diameter = 5.0
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, base_radius)
    .lineTo(tip_radius, base_radius)
    .lineTo(tip_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(tip_radius)
solid = solid.faces(">Z").workplane().hole(mount_hole_diameter)
vent_slot = (
    cq.Workplane("XY")
    .center(vent_slot_offset, vent_slot_height/2)
    .box(vent_slot_width, vent_slot_height, vent_slot_depth)
)
solid = solid.cut(vent_slot)
result = solid
