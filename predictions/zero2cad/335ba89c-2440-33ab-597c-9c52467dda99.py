import cadquery as cq

# Parameters
leg_length_long = 80.0
leg_length_short = 60.0
thickness = 8.0
extrude_length = 30.0
fillet_radius = 2.0
chamfer_distance = 1.0
hole_diameter = 5.0
hole_clearance = 5.5
cbore_diameter = 8.0
cbore_depth = 2.0
hole_offset_long = 20.0
hole_offset_short = 20.0
pocket_width = 30.0
pocket_height = 10.0
pocket_depth = 4.0

# L‑section profile (composite shape)
profile = [
    (0, 0),
    (leg_length_long, 0),
    (leg_length_long, thickness),
    (thickness, thickness),
    (thickness, leg_length_short),
    (0, leg_length_short),
]

# Base solid
result = (
    cq.Workplane("XY")
    .polyline(profile)
    .close()
    .extrude(extrude_length)
)

# Fillet all edges for safety
result = result.edges().fillet(fillet_radius)

# Mounting holes on long leg (top face)
result = (
    result.faces(">Z")
    .workplane()
    .moveTo(hole_offset_long, thickness / 2)
    .cboreHole(hole_clearance, cbore_diameter, cbore_depth)
)

# Mounting holes on short leg (top face)
result = (
    result.faces(">Z")
    .workplane()
    .moveTo(thickness / 2, hole_offset_short)
    .cboreHole(hole_clearance, cbore_diameter, cbore_depth)
)

# Pocket on inner face of long leg (negative Y side)
result = (
    result.faces("<Y")
    .workplane()
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)

# Chamfer outer edges for deburring
result = result.edges("|Z").chamfer(chamfer_distance)
