import cadquery as cq

outer_radius = 45
cap_height = 30
lip_height = 8
wall_thickness = 5
pocket_depth = 12
pocket_radius = outer_radius - wall_thickness - 3
rib_width = 4
rib_height = 6
rib_spacing_deg = 30
vent_slot_width = 2
vent_slot_length = 20
chamfer_distance = 2

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, cap_height - lip_height)
    .lineTo(outer_radius - wall_thickness, cap_height - lip_height)
    .lineTo(outer_radius - wall_thickness, cap_height)
    .lineTo(0, cap_height)
    .close()
)

base_solid = profile.revolve(360)

result = base_solid.faces(">Z").edges().chamfer(chamfer_distance)

pocket = (
    cq.Workplane("XY")
    .workplane(offset=cap_height - lip_height - pocket_depth)
    .circle(pocket_radius)
    .extrude(pocket_depth)
)

result = result.cut(pocket)

rib = (
    cq.Workplane("XZ")
    .moveTo(outer_radius - wall_thickness / 2, cap_height - lip_height - rib_height / 2)
    .rect(rib_width, rib_height)
    .extrude(wall_thickness)
)

rib_count = int(360 / rib_spacing_deg)
for i in range(rib_count):
    angle = i * rib_spacing_deg
    rotated_rib = rib.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(rotated_rib)

slot = (
    cq.Workplane("YZ")
    .rect(vent_slot_width, vent_slot_length)
    .extrude(wall_thickness * 2)
)

slot = slot.translate((outer_radius - wall_thickness / 2, 0, cap_height / 2))
slot_count = int(360 / (2 * rib_spacing_deg))
for j in range(slot_count):
    angle = j * (360 / slot_count)
    rotated_slot = slot.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(rotated_slot)
