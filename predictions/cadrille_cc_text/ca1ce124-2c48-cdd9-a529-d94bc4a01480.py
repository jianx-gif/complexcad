import cadquery as cq
length = 80.0
beam_width = 40.0
beam_height = 60.0
flange_thickness = 8.0
web_thickness = 6.0
fillet_radius = 2.0
hole_diameter = 5.0
hole_spacing = 20.0
rib_thickness = 4.0
rib_height = 30.0
rib_depth = 5.0
chamfer_distance = 1.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (web_thickness, 0),
        (web_thickness, beam_height),
        (web_thickness + flange_thickness, beam_height),
        (web_thickness + flange_thickness, beam_height - rib_depth),
        (0, beam_height - rib_depth),
        (0, 0)
    ])
    .close()
    .extrude(beam_width)
)
flange = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_depth)
)
flange = (
    flange.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
result = (
    flange.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
