import cadquery as cq

outer_radius = 40.0
wall_thickness = 3.0
inner_radius = outer_radius - wall_thickness
height = 60.0
fillet_radius = 1.0
boss_radius = 15.0
boss_height = 8.0
vent_slot_width = 4.0
vent_slot_height = 12.0
vent_slot_count = 12
vent_slot_depth = wall_thickness + 0.5

profile = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height)
    .lineTo(outer_radius, height)
    .lineTo(outer_radius, 0)
    .close()
)

shell = profile.revolve()

shell = shell.edges().fillet(fillet_radius)

boss = (
    cq.Workplane("XY")
    .center(inner_radius - boss_radius, 0)
    .circle(boss_radius)
    .extrude(boss_height)
)

shell = shell.union(boss)

slot = (
    cq.Workplane("XY")
    .center(outer_radius - wall_thickness/2, 0)
    .rect(vent_slot_width, vent_slot_height)
    .extrude(vent_slot_depth)
)

for i in range(vent_slot_count):
    angle = i * 360.0 / vent_slot_count
    shell = shell.cut(slot.rotate((0, 0, 0), (0, 0, 1), angle))

result = shell