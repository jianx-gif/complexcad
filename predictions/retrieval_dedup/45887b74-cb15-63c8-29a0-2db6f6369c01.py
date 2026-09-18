import cadquery as cq

# Parameters (mm, max dimension 100)
leg_length_x = 70.0
leg_length_y = 50.0
bracket_thickness = 10.0
gusset_height = 20.0
boss_radius = 8.0
boss_height = 12.0
fillet_radius = 6.0
hole_diameter = 6.0
hole_offset = 15.0
rib_thickness = 4.0
rib_width = 8.0
rib_spacing = 20.0

# L-shaped profile with integrated gusset and outer corner fillet
profile = (
    cq.Workplane('XY')
    .moveTo(0, 0)
    .lineTo(leg_length_x, 0)
    .lineTo(leg_length_x, bracket_thickness - fillet_radius)
    .radiusArc((leg_length_x - fillet_radius, bracket_thickness), fillet_radius)
    .lineTo(gusset_height, bracket_thickness)
    .lineTo(bracket_thickness, gusset_height)
    .lineTo(bracket_thickness, leg_length_y)
    .lineTo(0, leg_length_y)
    .close()
)
base = profile.extrude(bracket_thickness)
# Central boss on inner corner (adds volume and intersects base)
boss = (
    cq.Workplane('XY')
    .center(bracket_thickness, bracket_thickness)
    .circle(boss_radius)
    .extrude(boss_height)
)
base = base.union(boss)
# Mounting holes on horizontal leg (3 holes, cut through)
for i in range(3):
    y_pos = hole_offset + i * rib_spacing
    base = (
        base.faces('>Z')
        .workplane()
        .center(leg_length_x/2, y_pos)
        .hole(hole_diameter)
    )
# Mounting holes on vertical leg (2 holes, cut through)
for i in range(2):
    x_pos = hole_offset + i * rib_spacing
    base = (
        base.faces('>Z')
        .workplane()
        .center(x_pos, leg_length_y/2)
        .hole(hole_diameter)
    )
# Stiffening slots on inner face of horizontal leg (cut pockets)
num_slots_h = int((leg_length_x - 2 * hole_offset) // rib_spacing)
for i in range(num_slots_h):
    y_pos = hole_offset + i * rib_spacing + rib_spacing/2
    base = (
        base.faces('>Z')
        .workplane()
        .center(leg_length_x/2, y_pos)
        .rect(rib_thickness, rib_width)
        .cutBlind(-rib_thickness)
    )
# Stiffening slots on inner face of vertical leg (cut pockets)
num_slots_v = int((leg_length_y - 2 * hole_offset) // rib_spacing)
for i in range(num_slots_v):
    x_pos = hole_offset + i * rib_spacing + rib_spacing/2
    base = (
        base.faces('>Z')
        .workplane()
        .center(x_pos, leg_length_y/2)
        .rect(rib_width, rib_thickness)
        .cutBlind(-rib_thickness)
    )

result = base