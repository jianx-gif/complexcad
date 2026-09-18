import cadquery as cq

# Parameters
bracket_width = 60.0
bracket_height = 40.0
bracket_thickness = 8.0
rib_width = 4.0
rib_height = 4.0
rib_spacing = 10.0
rib_depth = 2.0
hole_diameter = 8.0
hole_offset = 6.0
chamfer_size = 0.4

# Base L‑shaped bracket profile
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (bracket_width, 0),
        (bracket_width, rib_height),
        (bracket_width + rib_width, rib_height),
        (bracket_width + rib_width, bracket_height),
        (0, bracket_height),
        (0, 0),
    ])
    .close()
    .extrude(bracket_thickness)
)

# Chamfer outer edges for safety
base = base.edges().chamfer(chamfer_size)

# Ribbed back: cut shallow ribs on the back face
rib_count = int((bracket_width - 2 * hole_offset) // rib_spacing) + 1
base = (
    base.faces(">Z")
    .workplane()
    .center(hole_offset, 0)
    .rarray(rib_spacing, 0, rib_count, 1)
    .rect(rib_depth, rib_height)
    .cutBlind(-rib_depth)
)

# Clearance holes (through all thickness)
hole_positions = [
    (hole_offset, hole_offset),
    (bracket_width - hole_offset, hole_offset),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

result = base
