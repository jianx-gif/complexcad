import cadquery as cq

clamp_length = 80
clamp_width = 30
clamp_thickness = 6
jaw_thickness = 8
central_hole_diameter = 12
central_hole_depth = 4
blind_hole_diameter = 5
blind_hole_depth = 5
blind_hole_spacing = 15
blind_hole_count = 4
rib_height = 4
rib_thickness = 2
chamfer_distance = 0.5
notch_radius = jaw_thickness / 2
tab_length = 20
tab_width = 10
tab_thickness = 4
hex_socket_diameter = 10
hex_socket_depth = 4
pocket_width = 20
pocket_length = 30
pocket_depth = 2

base = (
    cq.Workplane('XY')
    .rect(clamp_length, clamp_width)
    .extrude(clamp_thickness)
)

notch_cut = (
    base
    .faces('>X')
    .workplane()
    .center(0, 0)
    .circle(notch_radius)
    .cutBlind(clamp_thickness)
)

central_hole = (
    notch_cut
    .faces('>Z')
    .workplane()
    .hole(central_hole_diameter, central_hole_depth)
)

blind_holes = (
    central_hole
    .faces('>Z')
    .workplane()
    .center(-clamp_length / 4, 0)
    .rarray(blind_hole_spacing, 0, blind_hole_count, 1)
    .hole(blind_hole_diameter, blind_hole_depth)
)

ribs = (
    blind_holes
    .faces('<Z')
    .workplane()
    .rarray(20, 0, 2, 1)
    .rect(rib_thickness, rib_height)
    .extrude(clamp_thickness)
)

chamfered = (
    ribs
    .edges('|Z')
    .chamfer(chamfer_distance)
)

tab = (
    chamfered
    .faces('>X')
    .workplane()
    .rect(tab_width, tab_thickness)
    .extrude(tab_length)
)

hex_socket = (
    tab
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .polygon(6, hex_socket_diameter)
    .cutBlind(hex_socket_depth)
)

pocket = (
    hex_socket
    .faces('<Z')
    .workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_length)
    .cutBlind(pocket_depth)
)

result = pocket