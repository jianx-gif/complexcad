import cadquery as cq

conduit_length = 80.0
conduit_width = 40.0
conduit_height = 30.0
wall_thickness = 2.0
fillet_radius = 1.0
chamfer_distance = 0.5
clearance_hole_diameter = 4.0
clearance_hole_spacing = 20.0
tab_width = 20.0
tab_thickness = 5.0
tab_hole_diameter = 3.0

base = (
    cq.Workplane("XY")
    .rect(conduit_width, conduit_height)
    .extrude(conduit_length)
    .shell(-wall_thickness)
)

filleted = (
    base
    .faces(">Z")
    .edges()
    .fillet(fillet_radius)
)

with_tab = (
    filleted
    .faces(">Z")
    .workplane()
    .rect(tab_width, tab_thickness)
    .extrude(wall_thickness, combine=True)
)

add_tab_holes = (
    with_tab
    .faces("<Z")
    .workplane()
    .center(-tab_width/2 + tab_thickness/2, 0)
    .hole(tab_hole_diameter)
    .center(tab_width - tab_thickness, 0)
    .hole(tab_hole_diameter)
)

add_side_holes = (
    add_tab_holes
    .faces(">X")
    .workplane()
    .rarray(clearance_hole_spacing, 0, 2, 1)
    .hole(clearance_hole_diameter)
    .faces("<X")
    .workplane()
    .rarray(clearance_hole_spacing, 0, 2, 1)
    .hole(clearance_hole_diameter)
)

result = (
    add_side_holes
    .faces("<Z")
    .edges()
    .chamfer(chamfer_distance)
)
