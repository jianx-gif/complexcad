import cadquery as cq

outer_radius = 30.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
cap_height = 40.0
flange_height = 8.0
flange_outer_radius = 35.0
flange_inner_radius = outer_radius
chamfer_size = 2.0
rib_width = 6.0
rib_height = cap_height - 5.0
rib_thickness = 2.0
rib_count = 4
vent_slot_width = 4.0
vent_slot_height = 12.0
vent_slot_count = 6

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, cap_height - chamfer_size)
    .lineTo(inner_radius + chamfer_size, cap_height)
    .lineTo(inner_radius, cap_height)
    .close()
)

cap_body = profile.revolve()

flange = (
    cq.Workplane("XY")
    .circle(flange_outer_radius)
    .circle(flange_inner_radius)
    .extrude(flange_height)
    .translate((0, 0, cap_height))
)

result = cap_body.union(flange)

rib = (
    cq.Workplane("XY")
    .box(rib_thickness, rib_width, rib_height)
    .translate((outer_radius - rib_thickness/2, 0, rib_height/2))
)

ribs = rib
for i in range(1, rib_count):
    angle = 360.0 / rib_count * i
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

result = result.union(ribs)

vent = (
    cq.Workplane("XY")
    .box(wall_thickness + 0.2, vent_slot_width, vent_slot_height)
    .translate((inner_radius + wall_thickness/2, 0, cap_height/2))
)

vent_cuts = vent
for i in range(1, vent_slot_count):
    angle = 360.0 / vent_slot_count * i
    vent_cuts = vent_cuts.union(vent.rotate((0, 0, 0), (0, 0, 1), angle))

result = result.cut(vent_cuts)
