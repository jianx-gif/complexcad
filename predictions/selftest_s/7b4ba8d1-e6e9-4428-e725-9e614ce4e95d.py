import cadquery as cq

# --------------------------
# Parameter definitions
# --------------------------
bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 6.0
flange_height = 20.0
flange_thickness = 8.0
cavity_length = 50.0
cavity_width = 25.0
cavity_depth = 4.0
hole_dia = 6.0
hole_counter_sink_angle = 82.0
hole_offset_x = -20.0
rib_thickness = 3.0
rib_width = 6.0
rib_spacing = 12.0
chamfer_size = 1.0
slot_width = 4.0
slot_depth = flange_height - 2.0

# Derived values
available_length = bracket_length - 2 * flange_thickness
num_ribs = int(available_length // rib_spacing) + 1
slot_length = flange_thickness * 0.8

# --------------------------
# Base plate
# --------------------------
base = (
    cq.Workplane('XY')
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

# --------------------------
# Flanges (left and right)
# --------------------------
flange_profile = (
    cq.Workplane('XY')
    .rect(flange_thickness, bracket_width)
    .extrude(flange_height)
)

flange_left = flange_profile.translate((-bracket_length / 2 + flange_thickness / 2, 0, bracket_thickness / 2))
flange_right = flange_profile.translate((bracket_length / 2 - flange_thickness / 2, 0, bracket_thickness / 2))

bracket = base.union(flange_left).union(flange_right)

# --------------------------
# Central recessed cavity on top face
# --------------------------
bracket = (
    bracket
    .faces('>Z')
    .workplane()
    .rect(cavity_length, cavity_width)
    .cutBlind(-cavity_depth)
)

# --------------------------
# Countersunk hole through base plate
# --------------------------
bracket = (
    bracket
    .faces('>Z')
    .workplane()
    .center(hole_offset_x, 0)
    .cskHole(hole_dia, bracket_thickness, hole_counter_sink_angle)
)

# --------------------------
# Mounting slots on each flange (centered vertically on flange face)
# --------------------------
def add_slot(part, x_offset):
    return (
        part
        .faces('>Z')
        .workplane(offset=bracket_thickness / 2 + flange_height / 2)
        .center(x_offset, 0)
        .rect(slot_length, slot_width)
        .cutBlind(-slot_depth)
    )

bracket = add_slot(bracket, -bracket_length / 2 + flange_thickness / 2)
bracket = add_slot(bracket, bracket_length / 2 - flange_thickness / 2)

# --------------------------
# Chamfer outer edges for safety (applied before ribs to avoid tiny features)
# --------------------------
bracket = bracket.edges().chamfer(chamfer_size)

# --------------------------
# Stiffening ribs on underside (manual loop for reliability)
# --------------------------
rib = (
    cq.Workplane('XY')
    .rect(rib_width, rib_thickness)
    .extrude(bracket_thickness / 2)
    .translate((0, 0, -bracket_thickness / 4))
)

rib_compound = None
for i in range(num_ribs):
    x_offset = -bracket_length / 2 + flange_thickness + i * rib_spacing
    rib_piece = rib.translate((x_offset, 0, 0))
    if rib_compound is None:
        rib_compound = rib_piece
    else:
        rib_compound = rib_compound.union(rib_piece)

if rib_compound is not None:
    result = bracket.union(rib_compound)
else:
    result = bracket
