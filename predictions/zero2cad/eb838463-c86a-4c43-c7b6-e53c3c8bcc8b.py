import cadquery as cq

outer_radius = 45.0
inner_radius = 30.0
thickness = 10.0
wall_thickness = 2.0
slot_width = 4.0
slot_length = 15.0
slot_count = 12
fillet_radius = 1.5

base = cq.Workplane('XY').circle(outer_radius).extrude(thickness)
shell = base.shell(-wall_thickness)
slot_radius = (inner_radius + outer_radius) / 2.0
result = (
    shell
    .faces('>Z')
    .workplane()
    .center(slot_radius, 0)
    .rect(slot_width, slot_length)
    .polarArray(0, 0, 360, slot_count)
    .cutThruAll()
    .edges('|Z')
    .fillet(fillet_radius)
)
