import cadquery as cq

knob_outer_diameter = 70.0
knob_height = 30.0
wall_thickness = 2.0
annular_pocket_depth = 5.0
front_fillet_radius = 3.0
slot_width = 8.0
slot_height = 12.0
mount_hole_diameter = 5.0
chamfer_size = 0.5

def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

base = (
    cq.Workplane('XY')
    .circle(knob_outer_diameter / 2)
    .extrude(knob_height)
)

tab = (
    base
    .faces('>Z')
    .workplane()
    .center(knob_outer_diameter / 2, 0)
    .rect(slot_width, slot_height)
    .extrude(wall_thickness)
    .union()
)

with_hole = tab.hole(mount_hole_diameter)

pocket_outer_radius = (knob_outer_diameter / 2) - wall_thickness
pocketed = (
    with_hole
    .faces('>Z')
    .workplane()
    .circle(pocket_outer_radius)
    .cutBlind(annular_pocket_depth)
)

filleted = (
    pocketed
    .firstSolid()
    .edges('|Z')
    .fillet(front_fillet_radius)
)

result = (
    filleted
    .firstSolid()
    .edges('<Z')
    .chamfer(chamfer_size)
)
