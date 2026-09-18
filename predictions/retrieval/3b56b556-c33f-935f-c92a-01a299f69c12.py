import cadquery as cq

# Parameters
bracket_length = 70.0
bracket_width = 40.0
bracket_thickness = 12.0
lug_diameter = 20.0
lug_length = 30.0
hole_diameter = 6.5
hole_clearance = hole_diameter
hole_spacing_x = 15.0
hole_spacing_y = 20.0
fillet_radius = 2.0
chamfer_distance = 2.0
rib_thickness = 4.0
rib_height = 4.0
rib_spacing = 15.0
tab_thickness = 5.0
tab_height = 15.0
csk_diameter = 12.0
csk_angle = 82.0

offset_x_start = -bracket_length/2 + 20.0
offset_y_start = -bracket_width/2 + 15.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

# Ribs on bottom face
rib = (
    cq.Workplane("XY")
    .box(rib_thickness, bracket_width, rib_height, centered=(True, True, False))
)
rib_positions = [
    -bracket_length/2 + rib_spacing,
    0,
    bracket_length/2 - rib_spacing,
]
for x in rib_positions:
    base = base.union(rib.translate((x, 0, -rib_height)))

# Cylindrical lug on +X side
lug = (
    base.faces(">X").workplane()
    .center(0, 0)
    .circle(lug_diameter/2)
    .extrude(lug_length)
)
result = base.union(lug)

# Fillet on edges parallel to X (lug side transitions)
result = result.edges("|X").fillet(fillet_radius)

# Chamfer on lug end face (+X direction)
result = result.faces(">X").chamfer(chamfer_distance)

# Define hole positions
hole_coords = []
for row in range(2):
    y = offset_y_start + row * hole_spacing_y
    count = 3 if row == 0 else 2
    for i in range(count):
        x = offset_x_start + i * hole_spacing_x
        hole_coords.append((x, y))

central_hole = hole_coords[0]
other_holes = hole_coords[1:]

# Drill clearance holes for the non‑central positions
if other_holes:
    result = (
        result.faces(">Z").workplane()
        .pushPoints(other_holes)
        .hole(hole_clearance)
    )

# Countersunk hole for central position
result = (
    result.faces(">Z").workplane()
    .center(*central_hole)
    .cskHole(hole_clearance, csk_diameter, csk_angle, depth=bracket_thickness)
)

# Mounting tab on -X side
tab = (
    result.faces("<X").workplane()
    .rect(tab_thickness, bracket_width/2 - 5)
    .extrude(tab_height)
)
result = result.union(tab)

# Reinforcement fillet on top perimeter edges
result = result.faces(">Z").edges().fillet(1.0)
