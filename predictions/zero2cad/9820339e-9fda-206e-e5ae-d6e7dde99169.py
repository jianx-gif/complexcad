import cadquery as cq

knob_radius = 30.0
knob_height = 20.0
slot_width = 8.0
slot_depth = 6.0
slot_fillet = 1.0
base_fillet = 1.5
central_hole_dia = 5.0

def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

result = (
    cq.Workplane("XY")
    .circle(knob_radius)
    .extrude(knob_height)
    .faces(">Z")
    .workplane()
    .hole(central_hole_dia)
    .workplane()
    .center(knob_radius - slot_depth/2, 0)
    .rect(slot_depth, slot_width)
    .cutBlind(-knob_height)
    .firstSolid()
    .edges("|Z")
    .fillet(slot_fillet)
    .firstSolid()
    .faces("<Z")
    .edges()
    .fillet(base_fillet)
)
