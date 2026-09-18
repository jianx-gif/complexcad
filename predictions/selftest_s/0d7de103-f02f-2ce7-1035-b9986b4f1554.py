import cadquery as cq

base_width = 60
base_height = 30
base_depth = 12
corner_radius = 4
wall_thickness = 1.5
slot_width = 4
slot_length = 20
slot_offset = 8
center_hole_diameter = 6
chamfer_size = 0.8


def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

result = (
    cq.Workplane('XY')
    .rect(base_width, base_height)
    .extrude(base_depth)
    .edges('|Z')
    .fillet(corner_radius)
    .faces('>Z')
    .workplane()
    .center(0, -base_height/2 + slot_offset)
    .tag('slot_plane')
    .firstSolid()
    .edges('|Y')
    .chamfer(chamfer_size)
    .workplaneFromTagged('slot_plane')
    .center(-base_width/2 + wall_thickness + slot_width/2, 0)
    .rect(slot_width, slot_length)
    .cutBlind(-base_depth + wall_thickness)
    .faces('>Z')
    .workplane()
    .circle(center_hole_diameter/2)
    .cutBlind(-base_depth/2)
)
