import cadquery as cq
plate_width = 80.0
plate_depth = 60.0
plate_thickness = 5.0
central_cut_width = 30.0
central_cut_height = 20.0
hole_spacing_x = 25.0
hole_spacing_y = 25.0
hole_rows = 2
hole_cols = 3
tap_hole_dia = 5.0
tap_hole_depth = plate_thickness - 2.0
chamfer_size = 0.5
rib_width = 12.0
rib_thickness = 2.0
rib_height = plate_depth - 2.0
rib_spacing = 30.0
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(central_cut_width, central_cut_height)
    .cutBlind(-plate_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(plate_width, plate_depth)
    .cutBlind(-plate_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(tap_hole_dia)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
result = base.union(rib)
result = result.edges("|Z").chamfer(chamfer_size)
