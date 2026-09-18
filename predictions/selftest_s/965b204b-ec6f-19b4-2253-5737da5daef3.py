import cadquery as cq
from types import SimpleNamespace as Measures

measures = Measures(
    plate_length = 70.0,
    plate_width = 30.0,
    thickness = 3.0,
    chamfer = 2.0,
    rib_width = 10.0,
    rib_height = 20.0,
    rib_offset = 20.0,
    hole_diameter = 4.0,
    hole_spacing = 12.0,
    hole_count = 4,
    hole_edge_clearance = 5.0,
    fillet_radius = 1.0
)
m = measures

# Base plate
base = (
    cq.Workplane("XY")
    .box(m.plate_length, m.plate_width, m.thickness)
    .translate((0, 0, m.thickness/2))
)

# Apply 45° chamfer on the leading edge (long side) of the top face
chamfered = (
    base
    .faces(">Z")
    .edges("X")
    .chamfer(m.chamfer)
)

# Reinforced rib attached to top surface, centered along width
rib = (
    cq.Workplane("XY")
    .rect(m.rib_width, m.rib_height)
    .extrude(m.thickness)
    .translate((m.rib_offset, m.plate_width/2, m.thickness/2))
)

combined = chamfered.union(rib)

# Pattern of clearance holes on rib surface
holes = (
    combined
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .pushPoints([
        (m.rib_offset - (m.rib_width/2) + m.hole_edge_clearance + i * m.hole_spacing, 0)
        for i in range(m.hole_count)
    ])
    .hole(m.hole_diameter)
)

# Small fillet on rib side edges for safety
final = (
    holes
    .edges("Z")
    .fillet(m.fillet_radius)
)

result = final