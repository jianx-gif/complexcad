import cadquery as cq

# Parameters
outer_length = 80.0
outer_width = 50.0
outer_height = 20.0
wall_thickness = 2.0
rib_width = 4.0
rib_height = 3.0
rib_spacing = 6.0
rib_count = 5
fillet_radius = 2.0
chamfer_distance = 0.5

# Base solid
base = (
    cq.Workplane("XY")
    .box(outer_length, outer_width, outer_height, centered=(True, True, False))
)

# Hollow shell
hollow = base.shell(-wall_thickness)

# Ribbed base on interior bottom face
ribbed = (
    hollow
    .faces("<Z")
    .workplane()
    .rarray(rib_width + rib_spacing, 0, rib_count, 1, center=True)
    .rect(rib_width, outer_length - 2 * wall_thickness)
    .extrude(rib_height)
)

# Fillet rear vertical edges (rear = -Y face)
filleted = (
    ribbed
    .faces("<Y")
    .edges("|X")
    .fillet(fillet_radius)
)

# Chamfer top outer edges for safety
result = (
    filleted
    .faces(">Z")
    .edges("|X or |Y")
    .chamfer(chamfer_distance)
)
