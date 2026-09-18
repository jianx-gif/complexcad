import cadquery as cq
outer_radius = 45
cap_height = 30
lip_height = 8
wall_thickness = 5
pocket_depth = 12
rib_width = 4
rib_height = 6
rib_spacing_deg = 30
rib_count = 4
vent_slot_width = 2
vent_slot_length = 20
vent_slot_depth = wall_thickness
chamfer_distance = 2
outer_radius = outer_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
base = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, cap_height - lip_height)
    .lineTo(inner_radius, cap_height - lip_height)
    .lineTo(inner_radius, 0)
    .close()
)
base = base.cut(inner_radius)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
base = base.union(rib)
base = base.edges().chamfer(chamfer_distance)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_width)
)
base = base.union(rib)
base = base.edges().chamfer(chamfer_distance)
result = base
