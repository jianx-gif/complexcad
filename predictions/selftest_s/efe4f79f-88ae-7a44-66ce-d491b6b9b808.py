import cadquery as cq

# Adjustable Parameters
beam_length = 100.0
beam_height = 30.0
beam_width = 20.0
wall_thickness = 1.0
corner_radius = 2.0
chamfer_size = 0.5
notch_depth = 5.0
notch_height = 8.0
pocket_width = 40.0
pocket_height = 10.0
pocket_depth = 8.0
hole_diameter = 3.2
hole_rows = 5
hole_cols = 5
hole_spacing_x = 15.0
hole_spacing_y = 12.0

half_h = beam_height / 2.0
half_w = beam_width / 2.0

# Base profile (rectangular beam with side notch)
profile = (
    cq.Workplane("XY")
    .moveTo(-half_h, -half_w)
    .lineTo(half_h - notch_depth, -half_w)
    .lineTo(half_h - notch_depth, -notch_height / 2.0)
    .lineTo(half_h, -notch_height / 2.0)
    .lineTo(half_h, notch_height / 2.0)
    .lineTo(half_h - notch_depth, notch_height / 2.0)
    .lineTo(half_h - notch_depth, half_w)
    .lineTo(-half_h, half_w)
    .close()
)

# Extrude to create solid beam
result = (
    profile
    .extrude(beam_length)
    # Thin-wall shell
    .shell(-wall_thickness, kind="intersection")
    # Outer edge chamfer for safety
    .edges("|Z")
    .chamfer(chamfer_size)
    # Central pocket on the inner face (+X direction)
    .faces(">X")
    .workplane()
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
    # Clearance holes array on the +Y side
    .faces(">Y")
    .workplane()
    .rarray(hole_spacing_x, hole_spacing_y, hole_cols, hole_rows)
    .hole(hole_diameter)
)
