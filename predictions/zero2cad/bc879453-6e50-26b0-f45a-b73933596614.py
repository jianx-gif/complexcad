import cadquery as cq

outer_diameter = 80.0
wall_thickness = 4.0
cap_height = 30.0
flange_height = 5.0
flange_extension = 12.0
vent_slot_width = 6.0
vent_slot_height = 12.0
vent_slot_count = 8
chamfer_size = 1.0

outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
flange_outer_radius = outer_radius + flange_extension

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, cap_height - flange_height)
    .lineTo(flange_outer_radius, cap_height - flange_height)
    .lineTo(flange_outer_radius, cap_height)
    .lineTo(0, cap_height)
    .close()
)

solid = profile.revolve()

hollow = solid.shell(-wall_thickness)

slot = (
    cq.Workplane("XY")
    .center(outer_radius - wall_thickness / 2.0, 0)
    .rect(vent_slot_width, vent_slot_height)
    .extrude(wall_thickness * 2.0)
)

result = hollow
for i in range(vent_slot_count):
    angle = i * 360.0 / vent_slot_count
    result = result.cut(slot.rotate((0, 0, 0), (0, 0, 1), angle))

result = result.faces(">Z").edges().chamfer(chamfer_size)
