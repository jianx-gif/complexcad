
import cadquery as cq

body_length = 60.0
body_radius = 12.0
inlet_radius = 6.0
inlet_length = 20.0
flange_radius = 30.0
flange_thickness = 8.0
fillet_radius = 2.0
outlet_thread_dia = 8.0
outlet_thread_length = 12.0
mount_hole_dia = 4.0
mount_hole_radius = 20.0
mount_hole_count = 4

valve_body = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(flange_radius, 0)
    .lineTo(flange_radius, flange_thickness)
    .lineTo(body_radius, flange_thickness)
    .lineTo(body_radius, body_length - inlet_length)
    .lineTo(inlet_radius, body_length - inlet_length)
    .lineTo(inlet_radius, body_length)
    .lineTo(0, body_length)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

result = (
    valve_body
    .fillet(fillet_radius)
    .faces(">Y").first().workplane()
    .hole(outlet_thread_dia, depth=outlet_thread_length)
    .faces("<Y").first().workplane()
    .pushPoints([
        (mount_hole_radius, 0),
        (-mount_hole_radius, 0),
        (0, mount_hole_radius),
        (0, -mount_hole_radius),
    ])
    .hole(mount_hole_dia)
)
