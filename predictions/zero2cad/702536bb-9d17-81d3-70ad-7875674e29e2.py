import cadquery as cq

outer_diameter = 60.0
wall_thickness = 4.0
cap_height = 30.0
rib_height = 10.0
rib_thickness = 2.0
rib_base_z = 10.0
vent_slot_width = 6.0
vent_slot_height = 3.0
vent_slot_count = 8
vent_slot_z = 15.0
screw_hole_diameter = 5.0
countersink_diameter = 10.0
countersink_angle = 82.0
screw_hole_depth = cap_height

outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, rib_base_z)
    .lineTo(outer_radius + rib_thickness, rib_base_z)
    .lineTo(outer_radius + rib_thickness, rib_base_z + rib_height)
    .lineTo(outer_radius, rib_base_z + rib_height)
    .lineTo(outer_radius, cap_height)
    .lineTo(inner_radius, cap_height)
    .close()
)

solid = profile.revolve()

vent_cuts = (
    cq.Workplane("XY")
    .workplane(offset=vent_slot_z)
    .polarArray(radius=outer_radius - wall_thickness/2, startAngle=0, angle=360, count=vent_slot_count)
    .rect(vent_slot_width, vent_slot_height)
    .extrude(-wall_thickness)
)

solid = solid.cut(vent_cuts)

solid = (
    solid.faces(">Z")
    .workplane()
    .center(outer_radius - wall_thickness/2, 0)
    .cskHole(screw_hole_diameter, countersink_diameter, countersink_angle, screw_hole_depth)
)

result = solid