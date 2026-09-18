import cadquery as cq

knob_length = 45.0
knob_radius = 20.0
flange_outer_radius = 30.0
flange_thickness = 8.0
pocket_width = 12.0
pocket_depth = 6.0
fillet_radius = 2.0
chamfer_distance = 0.5

# Helper to retrieve the first solid for edge operations
def first_solid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.first_solid = first_solid

# Build profile for revolved knob with subtle contour
profile = (
    cq.Workplane('XZ')
    .moveTo(0, 0)
    .lineTo(0, knob_length - flange_thickness)
    .lineTo(knob_radius, knob_length - flange_thickness)
    .threePointArc((knob_radius + 5, knob_length - flange_thickness/2), (knob_radius, 0))
    .close()
)

knob_body = profile.revolve()

# Add external flange on top of knob using a transformed workplane
with_flange = (
    knob_body
    .transformed(offset=(0, 0, knob_length - flange_thickness))
    .workplane()
    .circle(flange_outer_radius)
    .extrude(flange_thickness)
)

# Create relief pocket on top planar face of flange
with_pocket = (
    with_flange
    .faces('>Z')
    .workplane()
    .rect(pocket_width, pocket_depth)
    .cutBlind(-pocket_depth)
)

# Apply fillet to outer edges parallel to Z and chamfer to top edge
result = (
    with_pocket
    .first_solid()
    .edges('|Z')
    .fillet(fillet_radius)
    .first_solid()
    .edges('>Z')
    .chamfer(chamfer_distance)
)
