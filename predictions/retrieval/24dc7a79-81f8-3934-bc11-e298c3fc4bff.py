import cadquery as cq
panel_width = 80
panel_height = 50
panel_thickness = 5
corner_radius = 5
hole_diameter = 10
hole_spacing = 12
num_holes = 5
hole_offset_y = -panel_height/2 + 10
tab_thickness = 5
tab_height = 10
chamfer_distance = 0.2
# Base panel with filleted corner on all outer edges
base = (
    cq.Workplane('XY')
    .rect(panel_width, panel_height)
    .extrude(panel_thickness)
    .edges('|Z')
    .fillet(corner_radius)
)
# Recessed pocket
pocket_width = 30
pocket_depth = 10
base = (
    base
    .faces('>Z')
    .workplane()
    .rect(pocket_width, pocket_depth)
    .cutBlind(pocket_depth)
)
# Linear clearance holes
hole_start_x = -((num_holes-1)*hole_spacing)/2
base = (
    base
    .faces('>Z')
    .workplane()
    .center(hole_start_x, hole_offset_y)
    .rarray(hole_spacing, 0, num_holes, 1)
    .hole(hole_diameter)
)
# Mounting tab on left side with chamfer
tab = (
    cq.Workplane('XY')
    .box(tab_thickness, tab_height, panel_thickness)
    .edges('|Z')
    .chamfer(chamfer_distance)
    .translate((-panel_width/2 - tab_thickness/2, 0, 0))
)
result = base.union(tab)
