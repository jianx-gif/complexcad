import cadquery as cq

knob_diameter = 60.0
knob_length = 30.0
wall_thickness = 2.0
pocket_radius = 10.0
pocket_width = pocket_radius * 2
pocket_depth = 5.0
through_hole_diameter = 4.0
fillet_radius = 1.0
chamfer_distance = 0.5
rib_width = 8.0
rib_length = 20.0
rib_height = 3.0
slot_width = 6.0
slot_length = 12.0
slot_depth = 4.0


def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

knob = (
    cq.Workplane("XY")
    .circle(knob_diameter / 2)
    .extrude(knob_length)
)

knob = (
    knob
    .edges()
    .chamfer(chamfer_distance)
)

knob = (
    knob
    .faces(">Z")
    .workplane()
    .tag("top_face")
)

knob = (
    knob
    .workplane()
    .center(knob_diameter / 2 - pocket_depth / 2, 0)
    .transformed(rotate=(0, 90, 0))
    .rect(pocket_width, pocket_depth)
    .cutBlind(-pocket_depth)
)

knob = (
    knob
    .edges("|Y")
    .fillet(fillet_radius)
)

knob = (
    knob
    .workplaneFromTagged("top_face")
    .center(0, 0)
    .circle(through_hole_diameter / 2)
    .firstSolid()
    .cutThruAll()
)

knob = (
    knob
    .workplaneFromTagged("top_face")
    .center(0, 0)
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)

knob = (
    knob
    .workplane()
    .center(knob_diameter / 2 - slot_depth / 2, knob_length / 4)
    .transformed(rotate=(0, 90, 0))
    .rect(slot_width, slot_length)
    .cutBlind(-slot_depth)
)

result = knob