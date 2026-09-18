import cadquery as cq
knob_total_width = 80.0
knob_base_height = 30.0
knob_base_thickness = 6.0
central_boss_radius = 12.0
central_boss_height = 8.0
vent_slot_width = 5.0
vent_slot_height = 20.0
vent_slot_offset = 20.0
vent_slot_height = 20.0
edge_chamfer = 0.5
mount_hole_diameter = 6.0
rib_thickness = 1.5
rib_height = 4.0
rib_spacing = 15.0
base = (
    cq.Workplane("XY")
    .rect(knob_base_height, knob_base_height)
    .extrude(knob_base_thickness)
)
vent = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(central_boss_radius)
    .extrude(central_boss_height)
    .translate((0, 0, knob_base_height))
)
knob_body = base.union(vent)
vent = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(central_boss_radius)
    .extrude(central_boss_height)
    .translate((0, 0, knob_base_height))
)
result = base.union(vent)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(vent_slot_width, vent_slot_height)
    .cutBlind(-vent_slot_height)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(mount_hole_diameter / 2)
    .cutBlind(-mount_hole_diameter)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(mount_hole_diameter / 2)
    .cutBlind(-mount_hole_diameter)
)
