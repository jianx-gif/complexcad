import cadquery as cq
base_length = 80.0
base_width = 30.0
base_thickness = 6.0
frame_outer_radius = 12.0
frame_inner_radius = 15.0
frame_height = 8.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 12.0
hole_spacing_y = 15.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
frame = (
    base.faces(">Z").workplane()
    .rect(frame_outer_radius, frame_outer_radius)
    .extrude(frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .rect(frame_outer_radius, frame_outer_radius)
    .extrude(frame_height)
)
frame = (
    frame.faces(">Z").workplane()
    .rect(frame_outer_radius, frame_outer_radius)
    .cutBlind(-frame_height)
)
hole_positions = [
    (-hole_spacing_x/2, -hole_spacing_y/2),
    (hole_spacing_x/2, -hole_spacing_y/2),
    (-hole_spacing_x/2, hole_spacing_y/2),
    (hole_spacing_x/2, hole_spacing_y/2),
]
frame = (
    frame.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = (
    frame.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
