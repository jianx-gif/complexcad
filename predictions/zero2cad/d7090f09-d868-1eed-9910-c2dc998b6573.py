import cadquery as cq

# Parameters
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
base_height = 8.0
dome_height = 20.0
chamfer_size = 0.5
pocket_width = 25.0
pocket_length = 15.0
pocket_depth = 3.0
pocket_offset = 5.0

# Helper to get first solid
def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

# Build profile for revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, base_height)
    .threePointArc((outer_radius, base_height + dome_height/2), (outer_radius, base_height + dome_height))
    .lineTo(outer_radius, 0)
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

# Add recessed pocket on top surface
result = (
    knob_body
    .faces(">Z")
    .workplane()
    .center(0, outer_radius - pocket_offset)
    .rect(pocket_width, pocket_length)
    .cutBlind(-pocket_depth)
    .firstSolid()
    .edges()
    .chamfer(chamfer_size)
)
