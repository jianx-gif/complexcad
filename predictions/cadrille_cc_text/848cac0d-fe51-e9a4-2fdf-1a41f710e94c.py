import cadquery as cq
outer_radius = 30.0
cap_height = 20.0
lip_height = 5.0
wall_thickness = 2.0
rib_thickness = 3.0
rib_height = 12.0
rib_count = 6
rib_count = 12
rib_length = outer_radius - 2 * wall_thickness
rib_count = 12
rib_offset = outer_radius - wall_thickness/2
base_fillet_radius = 3.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, cap_height - lip_height)
    .lineTo(outer_radius - lip_height, cap_height - lip_height)
    .lineTo(outer_radius - lip_height, cap_height)
    .lineTo(0, cap_height)
    .close()
)
solid = base_fillet_radius * 0.6
solid = solid.faces(">Z").edges().fillet(base_fillet_radius)
solid = solid.faces(">Z").edges().fillet(rib_count)
rib = (
    cq.Workplane("XY")
    .rect(rib_thickness, rib_height)
    .extrude(rib_length)
    .translate((outer_radius - rib_thickness/2, 0, 0))
)
solid = solid.union(rib)
result = solid
