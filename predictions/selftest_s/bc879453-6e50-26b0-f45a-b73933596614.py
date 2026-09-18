import cadquery as cq
import math

outer_dia = 70.0
wall_thickness = 5.0
cap_height = 20.0
lip_extra = 10.0
lip_height = 4.0
lip_chamfer = 0.8
blind_hole_dia = 30.0
blind_hole_depth = 12.0
vent_slot_width = 6.0
vent_slot_depth = 3.0
num_vent_slots = 6

body = cq.Workplane("XY").circle(outer_dia/2).extrude(cap_height)
lip = cq.Workplane("XY").circle((outer_dia + 2*lip_extra)/2).extrude(lip_height).translate((0, 0, cap_height))
result = body.union(lip)
result = result.faces(">Z").edges().chamfer(lip_chamfer)
result = result.faces(">Z").workplane().center(0, 0).circle(blind_hole_dia/2).cutBlind(blind_hole_depth)
outer_radius = outer_dia/2
inner_radius = outer_radius - wall_thickness
slot_center_radius = inner_radius + vent_slot_depth/2
slot_height = cap_height + lip_height
for i in range(num_vent_slots):
    angle = i * 360.0 / num_vent_slots
    slot = (
        cq.Workplane("XY")
        .rect(vent_slot_width, slot_height)
        .extrude(vent_slot_depth)
        .translate((slot_center_radius, 0, 0))
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.cut(slot)
