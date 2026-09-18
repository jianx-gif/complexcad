import cadquery as cq

base_radius = 20
top_radius = 30
height = 50
fillet_radius = 2
chamfer_distance = 1
mount_hole_diameter = 5
slot_width = 10
slot_depth = 5


def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

result = (
    cq.Workplane("XY")
    .circle(base_radius)
    .workplane(offset=height)
    .circle(top_radius)
    .loft()
    .faces("<Z")
    .edges()
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .hole(mount_hole_diameter)
    .faces(">Z")
    .edges()
    .chamfer(chamfer_distance)
    .faces(">Z")
    .first()
    .workplane()
    .center(0, 0)
    .rect(slot_width, height/2)
    .cutBlind(-slot_depth)
)
