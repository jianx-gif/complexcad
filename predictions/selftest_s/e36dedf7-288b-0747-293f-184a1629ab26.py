import cadquery as cq

outer_diameter = 70.0
cap_height = 25.0
lip_height = 6.0
lip_thickness = 5.0
pilot_hole_diameter = 5.0
pilot_hole_depth = cap_height + lip_height
chamfer_distance = 1.0
rib_height = 8.0
rib_width = 3.0
rib_count = 6
relief_width = 20.0
relief_depth = 3.0
slot_width = 12.0
slot_depth = 4.0

outer_radius = outer_diameter / 2.0
lip_outer_radius = outer_radius + lip_thickness

profile = (
    cq.Workplane('XZ')
    .moveTo(0, 0)
    .lineTo(0, cap_height)
    .lineTo(outer_radius, cap_height)
    .lineTo(outer_radius, cap_height + lip_height)
    .lineTo(lip_outer_radius, cap_height + lip_height)
    .lineTo(lip_outer_radius, 0)
    .close()
)

solid = profile.revolve()

solid = solid.faces(">Z").workplane().cskHole(pilot_hole_diameter, pilot_hole_diameter*0.6, pilot_hole_depth)

solid = solid.faces(">Z").edges().chamfer(chamfer_distance)

rib_profile = (
    cq.Workplane('XZ')
    .moveTo(lip_outer_radius, cap_height * 0.2)
    .lineTo(lip_outer_radius + rib_height, cap_height * 0.2)
    .lineTo(lip_outer_radius + rib_height, cap_height * 0.2 + rib_width)
    .lineTo(lip_outer_radius, cap_height * 0.2 + rib_width)
    .close()
    .revolve()
)

result = solid
angle_step = 360.0 / rib_count
for i in range(rib_count):
    angle = i * angle_step
    result = result.union(rib_profile.rotate((0, 0, 0), (0, 0, 1), angle))

result = result.faces(">Z").workplane().rect(relief_width, relief_depth).cutBlind(-relief_depth)

result = result.faces(">Z").workplane(offset=-lip_height/2).rect(slot_width, slot_depth).cutBlind(-slot_depth)
