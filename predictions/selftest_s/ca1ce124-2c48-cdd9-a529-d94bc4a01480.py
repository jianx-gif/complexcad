import cadquery as cq

length = 80.0
beam_height = 60.0
beam_width = 40.0
flange_thickness = 8.0
web_thickness = 6.0
fillet_radius = 2.0
hole_diameter = 5.0
hole_spacing = 20.0
rib_thickness = 4.0
rib_height = 30.0
rib_depth = 5.0
chamfer_distance = 1.0

outer_half_width = beam_width / 2.0

pts = [
    (0, -beam_height / 2.0),
    (0, -flange_thickness / 2.0),
    (outer_half_width, -flange_thickness / 2.0),
    (outer_half_width, -flange_thickness / 2.0 + flange_thickness),
    (web_thickness, -flange_thickness / 2.0 + flange_thickness),
    (web_thickness, beam_height / 2.0 - flange_thickness),
    (outer_half_width, beam_height / 2.0 - flange_thickness),
    (outer_half_width, beam_height / 2.0),
    (0, beam_height / 2.0)
]

half_beam = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(length)
)

filleted_beam = half_beam.edges("|Z").fillet(fillet_radius)

bolt_pattern = (
    filleted_beam.faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .rarray(hole_spacing, 0, 2, 1, center=True)
    .hole(hole_diameter)
)

chamfered_beam = bolt_pattern.edges("|Z").chamfer(chamfer_distance)

result = (
    chamfered_beam.faces(">X")
    .workplane(offset=-web_thickness/2)
    .rect(rib_height, rib_depth)
    .cutBlind(rib_thickness)
)
