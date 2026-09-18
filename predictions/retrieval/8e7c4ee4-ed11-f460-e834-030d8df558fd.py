import cadquery as cq

# Parameters
body_diameter = 50.0
body_length = 80.0
wall_thickness = 5.0
outlet_diameter = 20.0
outlet_chamfer = 1.0
side_port_diameter = 12.0
seal_counterbore_diameter = 25.0
seal_counterbore_depth = 8.0
rib_width = 4.0
rib_height = 6.0
rib_spacing = 20.0
boss_diameter = 12.0
boss_height = 4.0

# Base valve body via revolve of a composite profile
profile = (
    cq.Workplane('XZ')
    .lineTo(0, body_length)
    .lineTo(body_diameter / 2, body_length)
    .lineTo(body_diameter / 2, 0)
    .close()
)
body = profile.revolve()

# Stepped outlet region at front (-Z)
outlet_step_len = 10.0
body = (
    body
    .faces('<Z')
    .workplane(offset=-outlet_step_len)
    .circle((outlet_diameter / 2) + wall_thickness)
    .cutBlind(outlet_step_len)
)

# Main outlet hole with chamfer on entry edge (select primary top face)
valve = (
    body
    .faces('>Z')
    .first()
    .workplane()
    .hole(outlet_diameter)
    .edges()
    .chamfer(outlet_chamfer)
)

# Counterbore for seal on rear face (select primary rear face)
valve = (
    valve
    .faces('<Z')
    .first()
    .workplane()
    .hole(seal_counterbore_diameter, depth=seal_counterbore_depth)
)

# Side circular port on the +X side wall (centered at front edge)
valve = (
    valve
    .faces('>X')
    .first()
    .workplane()
    .hole(side_port_diameter, depth=wall_thickness + 0.5)
)

# Add ribs on top surface for stiffness
num_ribs = int(body_diameter // rib_spacing)
for i in range(num_ribs):
    rib_x = (i + 0.5) * rib_spacing - body_diameter / 2
    valve = (
        valve
        .workplane(offset=body_length / 2)
        .center(rib_x, 0)
        .rect(rib_width, rib_height)
        .extrude(wall_thickness)
    )

# Sensor mounting boss on top face
valve = (
    valve
    .workplane(offset=body_length / 2)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

result = valve