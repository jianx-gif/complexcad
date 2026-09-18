import cadquery as cq

# Parameters
plate_length = 100.0
plate_width = 40.0
plate_thickness = 5.0
edge_margin = 8.0
hole_diameter = 5.0
countersink_diameter = 9.0
countersink_angle = 82
countersink_depth = 2.0
chamfer_size = 1.0
rib_height = 3.0
rib_thickness = 4.0
rib_length = plate_width - 2*edge_margin
boss_height = 4.0
boss_width = 20.0
pocket_width = 30.0
pocket_depth = 2.0
pocket_offset = 10.0

# Derived dimensions
hole_spacing = (plate_length - 2 * edge_margin) / (9 - 1)

# Base plate
result = (
    cq.Workplane('XY')
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
    .faces('>Z')
    .chamfer(chamfer_size)
    .faces('<Z')
    .chamfer(chamfer_size)
)

# Central boss for rigidity
result = (
    result
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .rect(boss_width, boss_width)
    .extrude(boss_height)
)

# Bottom ribs for stiffness (two ribs symmetrically placed)
rib_y_offset = (plate_width / 2) - edge_margin - (rib_thickness / 2)
for sign in [-1, 1]:
    result = (
        result
        .faces('<Z')
        .workplane()
        .center(0, sign * rib_y_offset)
        .rect(rib_thickness, rib_length)
        .extrude(rib_height)
    )

# Pocket cutout near one end for cable routing
result = (
    result
    .faces('>Z')
    .workplane()
    .center(-plate_length/2 + pocket_offset + pocket_width/2, 0)
    .rect(pocket_width, plate_width - 2*edge_margin)
    .cutBlind(-pocket_depth)
)

# Linear array of nine countersunk holes
result = (
    result
    .faces('>Z')
    .workplane()
    .center(-plate_length/2 + edge_margin, 0)
    .rarray(hole_spacing, 0, 9, 1)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle, countersink_depth)
)

# Small fillet on top edges for safety
result = (
    result
    .faces('>Z')
    .edges()
    .fillet(chamfer_size/2)
)
