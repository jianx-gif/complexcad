import cadquery as cq

# Parameters
leg_length = 80.0
leg_width = 20.0
extrude_depth = 30.0
wall_thickness = 2.0
inner_leg_width = leg_width - 2 * wall_thickness
inner_leg_length = leg_length - 2 * wall_thickness
relief_width = 6.0
relief_height = 4.0
relief_depth = 1.0
screw_hole_dia = 4.0
screw_hole_spacing = 20.0
screw_hole_edge_clearance = 5.0
chamfer_size = 0.5

# Outer L profile sketch
outer_profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg_width, 0)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width + leg_width, leg_length)
    .lineTo(leg_width + leg_width, leg_length + leg_width)
    .lineTo(0, leg_length + leg_width)
    .close()
)

# Inner L profile sketch (offset inward by wall_thickness)
inner_profile = (
    cq.Workplane("XY")
    .moveTo(wall_thickness, wall_thickness)
    .lineTo(wall_thickness + inner_leg_width, wall_thickness)
    .lineTo(wall_thickness + inner_leg_width, wall_thickness + inner_leg_length)
    .lineTo(wall_thickness + inner_leg_width + inner_leg_width, wall_thickness + inner_leg_length)
    .lineTo(wall_thickness + inner_leg_width + inner_leg_width, wall_thickness + inner_leg_length + inner_leg_width)
    .lineTo(wall_thickness, wall_thickness + inner_leg_length + inner_leg_width)
    .close()
)

# Extrude both profiles
outer_solid = outer_profile.extrude(extrude_depth)
inner_solid = inner_profile.extrude(extrude_depth)

# Thin‑walled L channel
result = outer_solid.cut(inner_solid)

# Relief cut on inner vertical face
result = (
    result
    .faces("<X")
    .workplane()
    .center(leg_width/2 + relief_width/2, extrude_depth/2)
    .rect(relief_width, relief_height)
    .cutBlind(-relief_depth)
)

# Screw holes on vertical leg outer face (+X)
vert_hole_positions = []
num_vert = int((leg_length - 2 * screw_hole_edge_clearance) / screw_hole_spacing) + 1
for i in range(num_vert):
    y = screw_hole_edge_clearance + i * screw_hole_spacing
    vert_hole_positions.append((y, extrude_depth/2))
result = (
    result
    .faces(">X")
    .workplane()
    .pushPoints(vert_hole_positions)
    .hole(screw_hole_dia)
)

# Screw holes on horizontal leg outer face (+Y)
horiz_hole_positions = []
num_horiz = int((leg_length - 2 * screw_hole_edge_clearance) / screw_hole_spacing) + 1
for i in range(num_horiz):
    x = screw_hole_edge_clearance + i * screw_hole_spacing
    horiz_hole_positions.append((x, extrude_depth/2))
result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints(horiz_hole_positions)
    .hole(screw_hole_dia)
)

# Chamfer outer edges parallel to Z
result = result.edges("|Z").chamfer(chamfer_size)
