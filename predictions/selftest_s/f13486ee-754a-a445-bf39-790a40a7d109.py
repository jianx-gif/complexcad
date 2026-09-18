import cadquery as cq

knob_radius = 20
knob_length = 50
wall_thickness = 2
flange_radius = 30
flange_thickness = 8
pocket_width = 10
pocket_depth = 4
pocket_offset = wall_thickness + pocket_width/2


def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

profile = (
    cq.Workplane('XZ')
    .moveTo(wall_thickness, 0)
    .lineTo(wall_thickness, knob_length - flange_thickness)
    .threePointArc((flange_radius, knob_length), (flange_radius, knob_length - flange_thickness/2))
    .lineTo(flange_radius, 0)
    .close()
)

result = (
    profile
    .revolve(360, (0, 0, 1))
    .firstSolid()
    .faces('>Z')
    .tag('top_face')
    .workplaneFromTagged('top_face')
    .center(pocket_offset, 0)
    .rect(pocket_width, pocket_depth)
    .cutBlind(pocket_depth)
)
