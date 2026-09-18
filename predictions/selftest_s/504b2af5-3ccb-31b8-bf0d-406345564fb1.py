import cadquery as cq

body_length = 80.0
body_width = 30.0
body_thickness = 6.0
shoulder_width = 12.0
shoulder_height = 15.0
fillet_radius = 2.0
hole_diameter = 6.0
hole_offset_along = 20.0
rib_thickness = 2.0
rib_width = 5.0
rib_offset_from_edge = 5.0

# Base block
base = (
    cq.Workplane("XY")
    .rect(body_length, body_width)
    .extrude(body_thickness)
)

# Shoulder on +Y side
shoulder = (
    base.faces(">Z").workplane()
    .center(0, (body_width - shoulder_width) / 2)
    .rect(body_length, shoulder_width)
    .extrude(shoulder_height)
)

# Union base and shoulder
body = base.union(shoulder)

# Fillet external edges
body = body.edges().fillet(fillet_radius)

# Add interior rib on bottom face
rib = (
    body.faces("<Z").workplane()
    .rect(body_length - 2 * rib_offset_from_edge, rib_width)
    .extrude(rib_thickness)
)

body = body.union(rib)

# Drill clearance hole through body and shoulder
hole = (
    body.faces(">Z").workplane()
    .center(body_length / 2 - hole_offset_along, 0)
    .hole(hole_diameter)
)

result = hole
