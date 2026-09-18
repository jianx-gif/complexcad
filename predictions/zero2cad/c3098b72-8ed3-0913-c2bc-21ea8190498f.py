import cadquery as cq

outer_radius = 40.0
wall_thickness = 3.0
inner_radius = outer_radius - wall_thickness
cap_height = 20.0
groove_width = 2.0
groove_depth = 1.5
groove_offset_from_top = 2.0
chamfer_size = 0.5
vent_slot_width = 5.0
vent_slot_height = 2.0
vent_slot_depth = wall_thickness + 0.5

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, cap_height - groove_offset_from_top - groove_depth)
    .lineTo(inner_radius + groove_width, cap_height - groove_offset_from_top - groove_depth)
    .lineTo(inner_radius + groove_width, cap_height - groove_offset_from_top)
    .lineTo(outer_radius, cap_height - groove_offset_from_top)
    .lineTo(outer_radius, 0)
    .close()
)

solid = profile.revolve()

solid = solid.faces(">Z").edges().chamfer(chamfer_size)

vent_cut = (
    cq.Workplane("XY")
    .box(vent_slot_depth, vent_slot_width, vent_slot_height)
    .translate((outer_radius - vent_slot_depth/2, 0, cap_height/2))
)

result = solid.cut(vent_cut)
