import cadquery as cq

# Parameters
outer_radius = 30.0
inner_radius = 20.0
height = 50.0
base_fillet_radius = 5.0
groove_depth = 2.0
groove_width = 4.0
groove_position = 20.0
chamfer_distance = 1.0

# Helper to get first solid
def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

# Build profile for revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height - base_fillet_radius)
    .threePointArc((outer_radius, height - base_fillet_radius), (outer_radius, height))
    .lineTo(outer_radius, 0)
    .threePointArc((inner_radius, -base_fillet_radius), (inner_radius, 0))
    .close()
)

# Revolve to create knob body
knob_body = (
    profile
    .revolve(360)
    .firstSolid()
    .faces(">Z")
    .edges()
    .chamfer(chamfer_distance)
)

# Create annular groove as a ring cut
outer_cyl = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(groove_width)
    .translate((0, 0, groove_position - groove_width/2))
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(outer_radius - groove_depth)
    .extrude(groove_width + 0.2)
    .translate((0, 0, groove_position - groove_width/2))
)
ring = outer_cyl.cut(inner_cyl)

# Subtract groove from knob body
result = knob_body.cut(ring)
