import cadquery as cq

# Parameters
bracket_width = 60.0
bracket_height = 30.0
bracket_thickness = 8.0
notch_width = 12.0
notch_height = 8.0
notch_depth = 4.0
cavity_width = 30.0
cavity_height = 15.0
cavity_depth = bracket_thickness - 2.0
tab_length = 20.0
tab_width = 10.0
hole_diameter = 5.0
countersink_diameter = 8.0
countersink_angle = 90.0
hole_edge_clearance = 6.0
tab_hole_edge_clearance = 4.0
fillet_radius = 0.8
chamfer_dist = 0.5

# Base plate
base = (
    cq.Workplane("XY")
    .rect(bracket_width, bracket_height)
    .extrude(bracket_thickness)
)

# Notch cutout (top-left corner)
notch_center_x = -bracket_width/2 + notch_width/2 + hole_edge_clearance
notch_center_y = bracket_height/2 - notch_height/2 - hole_edge_clearance
base = (
    base
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .pushPoints([(notch_center_x, notch_center_y)])
    .rect(notch_width, notch_height)
    .cutBlind(-notch_depth)
)

# Housing cavity pocket centered on plate
cav_center_x = 0
cav_center_y = 0
base = (
    base
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .pushPoints([(cav_center_x, cav_center_y)])
    .rect(cavity_width, cavity_height)
    .cutBlind(-cavity_depth)
)

# Mounting tab (right side)
base = (
    base
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .center(bracket_width/2, 0)
    .rect(tab_length, tab_width)
    .extrude(bracket_thickness)
)

# Countersunk holes on main plate (4 corners)
plate_holes = []
for sx in (-1, 1):
    for sy in (-1, 1):
        hx = sx * (bracket_width/2 - hole_edge_clearance)
        hy = sy * (bracket_height/2 - hole_edge_clearance)
        plate_holes.append((hx, hy))

base = (
    base
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .pushPoints(plate_holes)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle)
)

# Countersunk holes on mounting tab (2 holes)
tab_holes = [
    (bracket_width/2 + tab_length/2, -tab_width/2 + tab_hole_edge_clearance),
    (bracket_width/2 + tab_length/2,  tab_width/2 - tab_hole_edge_clearance),
]
base = (
    base
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .pushPoints(tab_holes)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle)
)

# Fillet vertical edges for safety
result = (
    base
    .edges("|Z")
    .fillet(fillet_radius)
)
