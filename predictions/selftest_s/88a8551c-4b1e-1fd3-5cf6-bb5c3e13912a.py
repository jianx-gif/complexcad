import cadquery as cq

# Parameters
plate_length = 80.0
plate_width = 100.0
plate_thickness = 8.0
rib_width = 10.0
rib_height = 6.0
rib_fillet_radius = 1.0
hole_diameter = 6.0
hole_rows = 2
hole_cols = 4
hole_spacing_x = 20.0
hole_spacing_y = 30.0
chamfer_size = 1.0
tab_length = 20.0
tab_width = 30.0
tab_thickness = plate_thickness
pocket_depth = 4.0
pocket_margin = 5.0

# Base plate
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_length, plate_thickness, centered=(True, True, False))
)

# Central rib on top surface (added before tab to keep +Y face simple)
result = (
    result
    .faces("+Z")
    .workplane()
    .box(plate_width, rib_width, rib_height, centered=(True, True, False))
    .edges("|Z")
    .fillet(rib_fillet_radius)
)

# Mounting tab on +Y side (created as separate solid and united)
tab = (
    cq.Workplane("XY")
    .box(tab_width, tab_length, tab_thickness, centered=(True, True, False))
    .translate((0, plate_length / 2 + tab_length / 2, 0))
)
result = result.union(tab)

# Drill 2x4 hole array through the entire thickness (including tab)
result = (
    result
    .faces("-Z")
    .workplane()
    .rarray(hole_spacing_x, hole_spacing_y, hole_cols, hole_rows, center=True)
    .hole(hole_diameter)
)

# Chamfer outer vertical edges for safety
result = (
    result
    .edges("|Z")
    .chamfer(chamfer_size)
)

# Underside pocket for weight reduction, leaving margin from edges
pocket_width = plate_width - 2 * pocket_margin
pocket_length = plate_length - 2 * pocket_margin
result = (
    result
    .faces("-Z")
    .workplane()
    .rect(pocket_width, pocket_length)
    .cutBlind(-pocket_depth)
)
