import cadquery as cq
outer_diameter = 70.0
cap_height = 25.0
lip_height = 6.0
lip_thickness = 5.0
chamfer_distance = 1.0
rib_width = 3.0
rib_height = 8.0
relief_width = 20.0
relief_depth = 3.0
relief_depth = 4.0
slot_width = 12.0
slot_depth = 4.0
slot_count = 6
slot_count = 4
outer_radius = outer_diameter / 2.0
inner_radius = pilot_hole_diameter / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, cap_height - lip_thickness)
    .lineTo(outer_radius, cap_height - lip_thickness)
    .lineTo(outer_radius, cap_height)
    .lineTo(inner_radius, cap_height)
    .close()
)
base = profile.revolve()
base = base.faces(">Z").workplane().hole(pilot_hole_diameter)
base = base.faces(">Z").workplane().rect(relief_width, relief_depth).cutBlind(-relief_depth)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_width / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
base = base.union(rib)
base = base.faces(">Z").workplane().polarArray(radius=slot_count, count=slot_count, startAngle=0, angle=360).rect(slot_width, slot_depth).cutBlind(-relief_depth)
result = base
