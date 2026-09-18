import cadquery as cq

knob_diameter = 80
knob_height = 30
finger_base_width = 50
finger_base_depth = 20
finger_step1_height = 8
finger_step2_height = 5
finger_narrow_width = 30
finger_narrow_depth = 15
clearance_diameter = 12
top_fillet_radius = 4
lower_chamfer = 1.5
slot_width = 8
slot_height = 12
slot_depth = 5


def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

base = (
    cq.Workplane("XY")
    .circle(knob_diameter / 2)
    .extrude(knob_height)
    .faces(">Z")
    .workplane()
    .tag("top_face")
)

finger1 = (
    base
    .workplaneFromTagged("top_face")
    .rect(finger_base_width, finger_base_depth)
    .extrude(finger_step1_height)
)

finger2 = (
    finger1
    .workplaneFromTagged("top_face")
    .rect(finger_narrow_width, finger_narrow_depth)
    .extrude(finger_step2_height)
)

with_hole = (
    finger2
    .workplaneFromTagged("top_face")
    .hole(clearance_diameter)
)

# Helper to add a side slot using transformed workplane
def add_side_slot(part, rotation_y):
    return (
        part
        .workplaneFromTagged("top_face")
        .transformed(rotate=(0, rotation_y, 0))
        .center(knob_diameter / 2 - slot_depth, 0)
        .rect(slot_width, slot_height)
        .cutBlind(-slot_depth)
    )

slots_plus = add_side_slot(with_hole, -90)
slots = add_side_slot(slots_plus, 90)

filleted = (
    slots
    .firstSolid()
    .faces(">Z")
    .edges()
    .fillet(top_fillet_radius)
)

final = (
    filleted
    .firstSolid()
    .faces("<Z")
    .edges()
    .chamfer(lower_chamfer)
)

result = final