import cadquery as cq

# Parameters
plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
pocket_length = 40.0
pocket_width = 30.0
pocket_depth = 4.0
pocket_chamfer = 1.0
hole_diameter = 5.0
hole_offset = 12.0
rib_width = 6.0
rib_height = 4.0
rib_offset = 10.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

# Recessed pocket with chamfered vertical edges
pocket = (
    cq.Workplane("XY")
    .rect(pocket_length, pocket_width)
    .extrude(pocket_depth)
    .edges("|Z")
    .chamfer(pocket_chamfer)
    .translate((0, 0, plate_thickness - pocket_depth))
)

# Subtract pocket from base
result = base.cut(pocket)

# Mounting holes at four corners
hole_positions = [
    (-plate_length/2 + hole_offset, -plate_width/2 + hole_offset),
    ( plate_length/2 - hole_offset, -plate_width/2 + hole_offset),
    ( plate_length/2 - hole_offset,  plate_width/2 - hole_offset),
    (-plate_length/2 + hole_offset,  plate_width/2 - hole_offset),
]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

# Reinforcement ribs on underside (two orthogonal ribs)
# Long rib along X direction
rib_long = (
    cq.Workplane("XY")
    .rect(plate_length - 2 * rib_offset, rib_width)
    .extrude(rib_height)
    .translate((0, -plate_width/2 + rib_offset + rib_width/2, -rib_height))
)
# Short rib along Y direction
rib_short = (
    cq.Workplane("XY")
    .rect(rib_width, plate_width - 2 * rib_offset)
    .extrude(rib_height)
    .translate((-plate_length/2 + rib_offset + rib_width/2, 0, -rib_height))
)
result = result.union(rib_long).union(rib_short)
