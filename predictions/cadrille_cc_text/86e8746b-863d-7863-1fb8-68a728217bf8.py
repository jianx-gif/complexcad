import cadquery as cq
body_length = 80.0
body_diameter = 30.0
body_diameter = 15.0
flange_thickness = 5.0
inlet_hole_diameter = 5.0
outlet_hole_offset = 0.0
outlet_hole_depth = 30.0
outlet_hole_count = 4
outlet_hole_z = body_diameter/2 - 10.0
pilot_hole_offset = 0.0
pilot_hole_depth = body_diameter/2 - 10.0
profile = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),
        (body_diameter/2, 0),
        (body_diameter/2, body_diameter/2 - flange_thickness),
        (body_diameter/2 + flange_thickness, body_diameter/2 - flange_thickness),
        (body_diameter/2 + flange_thickness, body_diameter/2 + flange_thickness),
        (body_diameter/2 + flange_thickness, body_diameter/2 + flange_thickness),
        (body_diameter/2 + flange_thickness, body_diameter/2 + flange_thickness),
        (body_diameter/2 + flange_thickness, body_diameter/2 + flange_thickness),
        (body_diameter/2 + flange_thickness, body_diameter/2 + flange_thickness),
        (body_diameter/2 + flange_thickness, body_diameter/2 + flange_thickness),
        (body_diameter/2 + flange_thickness, body_diameter/2 + flange_thickness),
        (body_diameter/2 + flange_thickness, body_diameter/2 + flange_thickness),
        (body_diameter/2 + flange_thickness, body_diameter/2 + flange_thickness),
        (body_diameter/2 + flange_thickness, body_diameter/2 + flange_thickness),
        (body_diameter/2 + flange_thickness, body_diameter/2 + flange_thickness),
        (body_diameter/2 + flange_thickness, body_diameter/2 + flange_thickness),
        (body_diameter/2 + flange_thickness, body_diameter/2 + flange_thickness),
        (body_diameter/2 + flange_thickness, body_diameter/2 + flange_thickness),
        (body_diameter/2 + flange_thickness, body_diameter/2 + fl8),
        (body_diameter/2 + flange_thickness, body_diameter/2 + fl8),
        (body_diameter/2 + flange_thickness, body_diameter/2 + fl8),
        (body_diameter/2 + flange_thickness, body_diameter/2 + fl8),
        (body_diameter/2 + flange_thickness, body_diameter/2 + fl8),
    ])
    .wire()
    .edges()
    .fillet(inlet_hole_diameter)
)
result = (
    body
    .faces(">Z")
    .workplane()
    .pushPoints([
        (0, 0),
        (0, body_diameter),
        (0, body_diameter),
    ])
    .hole(pilot_hole_diameter)
)
