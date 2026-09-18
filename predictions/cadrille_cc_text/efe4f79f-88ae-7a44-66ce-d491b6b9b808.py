import cadquery as cq
beam_length = 100.0
beam_height = 30.0
wall_thickness = 1.0
corner_radius = 2.0
chamfer_size = 0.5
notch_width = 20.0
notch_depth = 5.0
pocket_width = 40.0
pocket_height = 8.0
pocket_depth = 8.0
hole_diameter = 3.2
hole_spacing_x = 15.0
hole_spacing_y = 12.0
hole_rows = 2
hole_cols = 3
hole_spacing_y = 12.0
base = (
    cq.Workplane("XY")
    .rect(beam_length, beam_height)
    .extrude(beam_height)
)
base = base.edges("|Z").chamfer(chamfer_size)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(notch_width, notch_height)
    .cutBlind(-notch_depth)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
base = (
    base.faces("<Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(notch_width, notch_height)
    .cutBlind(-notch_depth)
)
result = base
