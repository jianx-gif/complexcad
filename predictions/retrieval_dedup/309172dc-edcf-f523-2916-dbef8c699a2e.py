import cadquery as cq
import math

clamp_radius = 30
clamp_length = 60
wall_thickness = 5
conical_angle_deg = 10
through_hole_dia = 12
chamfer_dist = 2
flange_outer_radius = 40
flange_inner_radius = clamp_radius - wall_thickness
flange_thickness = 8
taper_length = 20
slot_width = 8
slot_length = 20
slot_depth = wall_thickness - 1
mount_hole_dia = 4
mount_hole_count = 4

taper_rad = math.radians(conical_angle_deg)
outer_top_radius = clamp_radius - taper_length * math.tan(taper_rad)
inner_bottom_radius = clamp_radius - wall_thickness
inner_top_radius = outer_top_radius - wall_thickness

result = (
    cq.Workplane("XZ")
    .moveTo(inner_bottom_radius, 0)
    .lineTo(clamp_radius, 0)
    .lineTo(outer_top_radius, clamp_length)
    .lineTo(inner_top_radius, clamp_length)
    .close()
    .revolve()
    .hole(through_hole_dia)
    .edges(">Z").chamfer(chamfer_dist)
    .faces("<Z").workplane()
    .circle(flange_outer_radius)
    .circle(flange_inner_radius)
    .extrude(flange_thickness)
    .faces(">X").first().workplane()
    .center(clamp_radius - wall_thickness/2, 0)
    .rect(slot_width, slot_length)
    .cutBlind(-slot_depth)
    .faces(">X").first().workplane()
    .polarArray(radius=clamp_radius - wall_thickness/2, count=mount_hole_count, startAngle=0, angle=360)
    .hole(mount_hole_dia)
)
