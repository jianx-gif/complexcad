import cadquery as cq

# Parameters
cap_outer_dia = 40.0
cap_height = 20.0
wall_thickness = 2.0
rib_thickness = 1.5
rib_width = 3.0
rib_height = 4.0
front_radius = 12.0
chamfer_size = 0.5

# Helper to get the first solid
def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

# Base solid (solid cylinder that will be shelled)
base = (
    cq.Workplane('XY')
    .circle(cap_outer_dia / 2)
    .extrude(cap_height)
)

# Shell to create hollow interior
hollow = (
    base
    .firstSolid()
    .shell(-wall_thickness)
)

# Add peripheral rib (ring extruded outward)
rib = (
    cq.Workplane('XY')
    .circle((cap_outer_dia / 2) - rib_width/2)
    .circle((cap_outer_dia / 2) - rib_width/2 - rib_thickness)
    .extrude(rib_height)
)

# Fuse rib to hollow body
body_with_rib = hollow.union(rib)

# Add rounded front using a spherical cap
rounded_front = (
    cq.Workplane('XY')
    .center(0, 0)
    .sphere(front_radius)
    .translate((0, 0, cap_height - front_radius))
)

# Intersect rounded front with body to achieve rounded top surface (cut away excess)
result = (
    body_with_rib
    .cut(rounded_front)
    .firstSolid()
    .faces('>Z')
    .chamfer(chamfer_size)
)
