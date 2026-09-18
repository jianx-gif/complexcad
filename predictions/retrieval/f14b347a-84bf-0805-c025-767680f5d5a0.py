import cadquery as cq
# dimensions
leg_length = 80.0
leg_width = 40.0
thickness = 8.0
fillet_radius = 1.0
chamfer_distance = 0.5
hole_diameter = 5.5  # clearance for M5 screw
hole_spacing = 30.0
hole_depth = 12.0
nut_pocket_flat = 8.0  # across flats for M5 nut
nut_pocket_depth = 4.0
# groove dimensions
groove_width = 6.0
groove_depth = 2.0
groove_offset_from_edge = 10.0
# create L cross‑section points (outer profile)
points = [
    (0, 0),
    (leg_width, 0),
    (leg_width, thickness),
    (thickness, thickness),
    (thickness, leg_length),
    (0, leg_length),
    (0, 0),
]
result = cq.Workplane('XY').polyline(points).close().extrude(thickness)
# fillet interior corner for strength
result = result.edges('<<Z').fillet(fillet_radius)
# chamfer outer edges for safety
result = result.edges('>>Z').chamfer(chamfer_distance)
# groove on outer leg (vertical leg)
# locate groove centre on outer leg along Y direction
groove_center_y = leg_length/2
result = result.faces('>Z').workplane(invert=True, origin=(thickness+groove_offset_from_edge+groove_width/2, groove_center_y, 0)).rect(groove_width, leg_width, centered=True).cutBlind(groove_depth)
# mounting holes on each leg (two per leg)
# holes on horizontal leg
result = (
    result
    .faces('>Y')
    .workplane()
    .pushPoints([ (leg_width/2, thickness/2), (-leg_width/2, thickness/2) ])
    .circle(hole_diameter/2)
    .cutBlind(-hole_depth)
)
# holes on vertical leg
result = (
    result
    .faces('>X')
    .workplane()
    .pushPoints([ (thickness/2, leg_length/2), (thickness/2, -leg_length/2) ])
    .circle(hole_diameter/2)
    .cutBlind(-hole_depth)
)
# nut pockets for M5 nuts on both legs
nut_radius = nut_pocket_flat * (2/ (3**0.5)) / 2  # convert across flats to circumradius, then radius
result = (
    result
    .faces('>Y')
    .workplane()
    .pushPoints([ (leg_width/2, thickness/2), (-leg_width/2, thickness/2) ])
    .polygon(6, nut_pocket_flat * (2/ (3**0.5)))
    .cutBlind(-nut_pocket_depth)
)
result = (
    result
    .faces('>X')
    .workplane()
    .pushPoints([ (thickness/2, leg_length/2), (thickness/2, -leg_length/2) ])
    .polygon(6, nut_pocket_flat * (2/ (3**0.5)))
    .cutBlind(-nut_pocket_depth)
)
