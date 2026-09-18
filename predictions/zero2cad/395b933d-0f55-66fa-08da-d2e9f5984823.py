import cadquery as cq

# Parameters
outer_diameter = 60.0
wall_thickness = 2.5
height = 30.0
rib_width = 8.0
rib_height = 3.0
rib_length = 30.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 20.0

# Helper to get first solid
def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

# Base hollow cylinder
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle((outer_diameter / 2) - wall_thickness)
    .extrude(height)
)

# Chamfer top outer edge
base = (
    base
    .faces(">Z")
    .edges()
    .chamfer(chamfer_size)
)

# Tag top face for later workplane
base = (
    base
    .faces(">Z")
    .workplane()
    .tag("top_wp")
)

# Add two mounting holes on top face
base = (
    base
    .workplaneFromTagged("top_wp")
    .center(-hole_spacing/2, 0)
    .hole(hole_diameter)
    .center(hole_spacing, 0)
    .hole(hole_diameter)
)

# Create rib profile on side
rib = (
    cq.Workplane("XZ")
    .rect(rib_height, rib_width)
    .extrude(rib_length)
)

# Position ribs on opposite sides of cylinder
rib1 = (
    rib
    .translate((outer_diameter/2 - wall_thickness/2, 0, 0))
)

rib2 = (
    rib
    .rotate((0,0,0), (0,0,1), 180)
    .translate((-(outer_diameter/2 - wall_thickness/2), 0, 0))
)

# Combine ribs with base
result = base.union(rib1).union(rib2)
