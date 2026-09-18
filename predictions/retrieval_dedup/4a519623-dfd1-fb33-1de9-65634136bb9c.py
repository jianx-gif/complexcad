import cadquery as cq
# Core dimensions (max 100 units)
beam_length = 80.0
web_height = 60.0
flange_width = 30.0
flange_thickness = 8.0
web_thickness = 6.0
shell_thickness = 1.5
hole_diameter = 8.0
# Derived dimensions
web_half = web_thickness / 2.0
# Half‑section points (clockwise from bottom center)
pts_half = [
    (0, -web_height/2),
    (0, -web_height/2 + flange_thickness),
    (web_half, -web_height/2 + flange_thickness),
    (flange_width, -web_height/2 + flange_thickness),
    (flange_width, web_height/2 - flange_thickness),
    (web_half, web_height/2 - flange_thickness),
    (0, web_height/2 - flange_thickness),
    (0, web_height/2),
    (0, -web_height/2)
]
result = (
    cq.Workplane('XY')
    .polyline(pts_half)
    .close()
    .mirrorY()
    .extrude(beam_length)
    .shell(-shell_thickness)
    .faces('>X')
    .workplane()
    .hole(hole_diameter)
)
