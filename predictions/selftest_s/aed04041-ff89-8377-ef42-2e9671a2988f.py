import cadquery as cq
plate_width = 80
plate_depth = 60
plate_thickness = 5
central_cut_width = 30
central_cut_height = 20
hole_spacing_x = 25
hole_spacing_y = 25
hole_cols = 3
hole_rows = 2
tap_hole_dia = 5
slot_length = 70
slot_width = 4
chamfer_size = 0.5
rib_thickness = 2
rib_width = 12
rib_spacing = 30
# base plate
base = (
    cq.Workplane('XY')
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
)
# central cutout through plate
base = (
    base
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .rect(central_cut_width, central_cut_height)
    .cutBlind(plate_thickness)
)
# tapped hole pattern on top
base = (
    base
    .faces('>Z')
    .workplane()
    .rarray(hole_spacing_x, hole_spacing_y, hole_cols, hole_rows, True)
    .hole(tap_hole_dia)
)
# narrow slot for threaded rod across top
base = (
    base
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .slot2D(slot_length, slot_width, 0)
    .cutThruAll()
)
# ribs on bottom face
ribs = (
    base
    .faces('<Z')
    .workplane()
    .rarray(rib_spacing, 0, 2, 1, True)
    .rect(rib_width, plate_depth - 2*slot_width)
    .extrude(rib_thickness)
)
# combine base and ribs
result = base.union(ribs)
# chamfer outer vertical edges
result = result.edges('|Z').chamfer(chamfer_size)
