import cadquery as cq

# Parameters
handle_length = 80.0
handle_width = 30.0
handle_thickness = 15.0
slot_width = 8.0
slot_length = 20.0
fillet_radius = 3.0
chamfer_distance = 2.0
mount_hole_dia = 5.0
mount_hole_spacing = 40.0
boss_dia = 12.0
boss_height = 5.0

# Base handle body created by extruding a rectangle profile
body = (
    cq.Workplane("XY")
    .rect(handle_width, handle_thickness)
    .extrude(handle_length)
)

# Side slot on the +Y face, centered along length
body = (
    body.faces(">Y")
    .workplane()
    .center(handle_length / 2, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-handle_thickness)
)

# Mounting holes on top (+Z) face, symmetrically placed
for x_offset in (-mount_hole_spacing / 2, mount_hole_spacing / 2):
    body = (
        body.faces(">Z")
        .workplane()
        .center(x_offset, 0)
        .hole(mount_hole_dia)
    )

# Central reinforcement boss on top face (adds to existing solid)
body = (
    body.faces(">Z")
    .workplane()
    .center(handle_length / 2, 0)
    .circle(boss_dia / 2)
    .extrude(boss_height)
)

# Chamfer on the front face (-Z) edges to reduce stress concentration
body = body.faces("<Z").edges().chamfer(chamfer_distance)

# Fillet on outer perimeter edges (excluding the side slot edge) for smoother stress distribution
body = body.edges("|Z and (>Y or <Y)").fillet(fillet_radius)

result = body