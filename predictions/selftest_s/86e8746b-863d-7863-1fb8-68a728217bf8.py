
import cadquery as cq

body_length = 80.0
body_diameter = 30.0
inlet_length = 20.0
inlet_diameter = 15.0
flange_thickness = 5.0
pilot_hole_diameter = 5.0
pilot_hole_depth = 30.0
chamfer_size = 2.0
pilot_hole_offset = 0.0

profile = [
    (0, flange_thickness),
    (inlet_length, inlet_diameter / 2),
    (inlet_length + body_length, body_diameter / 2),
    (inlet_length + body_length, -body_diameter / 2),
    (inlet_length, -inlet_diameter / 2),
    (0, -flange_thickness),
]

result = (
    cq.Workplane("XY")
    .polyline(profile)
    .close()
    .revolve()
    .workplane(offset=0)
    .transformed(rotate=cq.Vector(0, 90, 0))
    .center(pilot_hole_offset, 0)
    .hole(pilot_hole_diameter, pilot_hole_depth)
    .edges()
    .chamfer(chamfer_size)
)
