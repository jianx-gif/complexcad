import cadquery as cq

# Parameters
knob_outer_radius = 30.0
knob_height = 20.0
shaft_radius = 8.0
shaft_length = 12.0
wall_thickness = 2.0
chamfer_size = 1.0
slot_width = 4.0
slot_length = 12.0
slot_depth = 2.0
slot_count = 6
mount_hole_diameter = 3.0
mount_hole_offset = 15.0

# Helper to get first solid
def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

# Build profile for revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(shaft_radius, 0)
    .lineTo(shaft_radius, shaft_length)
    .threePointArc((knob_outer_radius, shaft_length + 2), (knob_outer_radius, shaft_length + 8))
    .lineTo(0, knob_height)
    .close()
)

# Revolve to create knob body
knob_body = (
    profile
    .revolve(360)
    .firstSolid()
    .faces("<Z")
    .chamfer(chamfer_size)
)

# Add mounting holes on top face
knob_with_holes = (
    knob_body
    .workplane(offset=knob_height)
    .pushPoints([(-mount_hole_offset, 0), (mount_hole_offset, 0)])
    .hole(mount_hole_diameter)
)

# Add grip slots on outer cylindrical surface
result = (
    knob_with_holes
    .faces("|Z")
    .workplane()
    .polarArray(radius=knob_outer_radius - wall_thickness/2, startAngle=0, angle=360, count=slot_count)
    .rect(slot_width, slot_length)
    .cutBlind(-slot_depth)
)
