import cadquery as cq
outer_radius = 30.0
height = 45.0
rim_fillet = 0.8
wall_thickness = 2.0
rib_radius = 10.0
rib_height = 6.0
slot_width = 3.0
slot_height = 10.0
slot_count = 6
slot_count = 12
slot_depth = wall_thickness + 2.0
rib_count = 4
rib_radius = outer_radius - wall_thickness
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(outer_radius + rim_fillet, height)
    .lineTo(outer_radius + rim_fillet, height)
    .lineTo(outer_radius, height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(rim_fillet)
solid = solid.faces(">Z").workplane().hole(2 * wall_thickness)
slot = (
    cq.Workplane("XY")
    .center(outer_radius + rim_fillet + slot_height / 2, 0)
    .rect(slot_width, slot_height)
    .extrude(slot_depth)
)
solid = solid.union(slot)
solid = solid.edges().fillet(rim_fillet)
result = solid
