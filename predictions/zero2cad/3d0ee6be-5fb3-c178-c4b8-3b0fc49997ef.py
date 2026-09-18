import cadquery as cq

# Parameters
knob_height = 40.0
bottom_radius = 15.0
top_radius = 22.0
wall_thickness = 2.0
fillet_radius = 1.5
chamfer_distance = 0.8
slot_width = 8.0
slot_length = 20.0
slot_depth = 4.0
central_hole_diameter = 4.0

# Helper to get the first solid from a selection
def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

# Base lofted knob body
base = (
    cq.Workplane("XY")
    .circle(bottom_radius)
    .workplane(offset=knob_height)
    .circle(top_radius)
    .loft()
    .firstSolid()
    .edges("<Z")
    .fillet(fillet_radius)
    .firstSolid()
    .faces(">Z")
    .chamfer(chamfer_distance)
)

# Tag the top face for later features
base = (
    base
    .faces(">Z")
    .workplane()
    .tag("top_face")
)

# Central through hole
base = (
    base
    .workplaneFromTagged("top_face")
    .hole(central_hole_diameter)
)

# Recessed slot on top surface
base = (
    base
    .workplaneFromTagged("top_face")
    .rect(slot_width, slot_length)
    .cutBlind(-slot_depth)
)

result = base